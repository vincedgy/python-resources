import concurrent.futures
import time
import boto3

ecr = boto3.client("ecr")


class ECRImage:
    def __init__(self, name, pushedAt, tags, image):
        self.image = image
        self.name = name
        self.pushedAt = pushedAt
        self.tags = tags

    def __repr__(self):
        return repr((self.image, self.name, self.pushedAt, self.tags))


repositories = {}


def getImages(repo):
    name = repo["repositoryName"]
    images = []
    r = ecr.describe_images(repositoryName=name)
    for image in r["imageDetails"]:
        try:
            images.append(
                ECRImage(
                    image=image["registryId"]
                    + ".dkr.ecr.eu-west-1.amazonaws.com/"
                    + image["repositoryName"]
                    + "@"
                    + image["imageTags"][0],
                    name=image["repositoryName"],
                    pushedAt=image["imagePushedAt"],
                    tags=image["imageTags"],
                )
            )
        except KeyError as exc:
            pass
    if len(images) > 0:
        return sorted(images, key=lambda image: image.pushedAt)
    else:
        return images


def main():
    start = time.perf_counter()
    print("Starting fetching all images in ECR")

    ecrRepositories = ecr.describe_repositories()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_images = {
            executor.submit(getImages, repo): repo
            for repo in ecrRepositories["repositories"]
        }
        for future in concurrent.futures.as_completed(future_to_images):
            repo = future_to_images[future]
            images = future.result()
            repositories[repo["repositoryName"]] = images

    end = time.perf_counter()

    for repository in repositories:
        for img in repositories[repository]:
            print(f"{img.image},{img.pushedAt}")

    print(f"Finished in {round(end-start,2)} second(s)")


if __name__ == "__main__":
    main()

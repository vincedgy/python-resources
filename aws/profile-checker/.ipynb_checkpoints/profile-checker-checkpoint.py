from pathlib import Path
import boto3
from botocore.exceptions import ClientError
import re

with open(str(Path.home()) + "/.aws/credentials", "r") as file:
    for line in file.readlines():
        try:
            profile = re.search(r"^\[(.+)\]", line).group(1)
            try:
                s3 = boto3.session.Session(
                    profile_name=profile, region_name="eu-west-1"
                ).resource("s3")
                response = s3.buckets.all()
                print(f"{profile}:OK")
            except ClientError as e:
                print(f"{profile}:KO")
        except:
            print("!")

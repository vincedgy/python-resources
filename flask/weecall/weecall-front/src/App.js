import React from "react";

function App() {
  const [buckets, setBuckets] = React.useState([]);

  React.useEffect(() => {
    fetch("http://127.0.0.1:5000/api/buckets")
      .then((res) => res.json())
      .then((r) => {
        setBuckets(r.data);
      });
  }, []);

  return (
    <div>
      <h1>Buckets</h1>
      <ul>
        {buckets.map((bucket) => (
          <li>{bucket.Name}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;

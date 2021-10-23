import { useEffect, useState } from "react";

const statusNew = 'new'
const statusReady = 'ready'

function ProgressChecker({ uuid, setAppState }) {
  const [progress, setProgress] = useState();

  useEffect(() => {
    fetch(`http://localhost:5000/progress?uuid=${uuid}`, {
      method: "get",
    })
      .then((response) => response.json())
      .then((result) => {
        console.log("Success:", result);
        setProgress(result);
        setAppState((state) => ({ ...state, progress: result }));
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, [uuid]);

  return (
    <div>
      {progress ? (
        <div>
          Распознано: {progress?.pages}/{progress?.ready}
        </div>
      ) : (
        "Загрузка..."
      )}
    </div>
  );
}

export default ProgressChecker;

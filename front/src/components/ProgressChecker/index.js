import { useState } from "react";
import { useInterval } from "react-use";
import statuses from "../../constants/statuses";
import Spinner from "../Spinner";

function ProgressChecker({ uuid, setAppState }) {
  const [progress, setProgress] = useState();

  const isReady = progress?.status === statuses.ready;

  useInterval(
    () => {
      if (uuid) {
        fetch(`${process.env.REACT_APP_API}/progress?uuid=${uuid}`, {
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
      }
    },
    isReady ? null : 5000
  );

  return (
    <div className="py-5 text-2xl">
      {progress ? (
        <div>
          {!isReady && <Spinner />}
          Преобразовано: {progress?.ready || 0} из {progress?.pages || 0}{" "}
          страниц
        </div>
      ) : (
        <>
          <Spinner />
          Загрузка...
        </>
      )}
    </div>
  );
}

export default ProgressChecker;

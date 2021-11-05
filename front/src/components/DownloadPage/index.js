import { useInterval } from "react-use";
import { useState } from "react";
import statuses from "../../constants/statuses";
import Spinner from "../Spinner";

function download(uuid, pageNumber) {
  fetch(`${process.env.REACT_APP_API}/file/${uuid}/${pageNumber}_new.jpg`, {
    method: "GET",
    headers: {},
  })
    .then((response) => {
      response.arrayBuffer().then(function (buffer) {
        const url = window.URL.createObjectURL(new Blob([buffer]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `${pageNumber}.jpg`); //or any other extension
        document.body.appendChild(link);
        link.click();
      });
    })
    .catch((err) => {
      console.log(err);
    });
}

function DownloadPage({ boxes, uuid, pageNumber }) {
  const [progress, setProgress] = useState({ status: statuses.ready });
  const isObfuscated = progress?.status === statuses.obfuscated;
  const isReady = progress?.status === statuses.ready;
  const inInProgress = progress?.status === statuses.in_progress;

  function handleDownload() {
    const body = {
      boxes: { nlp: boxes.filter((box) => box?.propn) },
    };
    fetch(`${process.env.REACT_APP_API}/process/${uuid}/${pageNumber}`, {
      method: "POST",
      headers: {
        Accept: "application/json, text/plain, */*",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    })
      .then((response) => response.json())
      .then((result) => {
        console.log("Success:", result);
        setProgress({});
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  useInterval(
    () => {
      if (uuid) {
        fetch(`${process.env.REACT_APP_API}/nlp/${uuid}/${pageNumber}`, {
          method: "get",
        })
          .then((response) => response.json())
          .then((result) => {
            // console.log("Success:", result);
            if (result.status === statuses.obfuscated) {
              download(uuid, pageNumber);
            }
            setProgress(result);
          })
          .catch((error) => {
            // console.error("Error:", error);
          });
      }
    },
    isReady || isObfuscated ? null : 3000
  );

  return (
    <>
      {isReady || isObfuscated ? (
        <button className="btn-blue w-full" disabled={inInProgress} onClick={handleDownload}>
          Скачать
        </button>
      ) : (
        <div className="p-4 text-gray-600 rounded-lg shadow bg-white">
          <Spinner /> Идет скачивание
        </div>
      )}
    </>
  );
}

export default DownloadPage;

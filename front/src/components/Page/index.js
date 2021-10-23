import { useEffect, useState } from "react";
import Canvas from "../Canvas";

function Page({ uuid, page, pageNumber }) {
  const [nlp, setNlp] = useState();

  useEffect(() => {
    fetch(`http://localhost:5000/nlp/${uuid}/${pageNumber}.json`, {
      method: "get",
    })
      .then((response) => response.json())
      .then((result) => {
        console.log("Success:", result);
        setNlp(result);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, [uuid]);

  function handleDownload(boxes) {
    const body = { boxes: { nlp: boxes.filter((box) => box?.propn) } };
    fetch(`http://localhost:5000/process/${uuid}/${pageNumber}`, {
      method: "post",
      body,
    })
      .then((response) => response.json())
      .then((result) => {
        console.log("Success:", result);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  return (
    <div>
      {`http://localhost:5000/file/${uuid}/${pageNumber}.jpg`}
      <Canvas
        handleDownload={handleDownload}
        nlpBoxes={nlp?.boxes?.nlp}
        src={`http://localhost:5000/file/${uuid}/${pageNumber}.jpg`}
      />
    </div>
  );
}

export default Page;

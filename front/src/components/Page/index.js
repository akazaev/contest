import { useState } from "react";
import Canvas from "../Canvas";
import { useInterval } from "react-use";
import statuses from "../../constants/statuses";

function Page({ uuid, page, pageNumber }) {
  const [nlp, setNlp] = useState();

  useInterval(
    () => {
      if (uuid) {
        fetch(`${process.env.REACT_APP_API}/nlp/${uuid}/${pageNumber}`, {
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
      }
    },
    nlp?.status === statuses.ready ? null : 5000
  );

  return (
    <Canvas
      nlpBoxes={nlp?.boxes?.nlp}
      pageNumber={pageNumber}
      uuid={uuid}
      pageStatus={nlp?.status}
    />
  );
}

export default Page;

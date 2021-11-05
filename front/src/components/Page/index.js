import Canvas from "../Canvas";
import { useInterval } from "react-use";
import statuses from "../../constants/statuses";

function Page({ uuid, page, pageIndex, handleEditPage }) {
  useInterval(
    () => {
      if (uuid) {
        fetch(`${process.env.REACT_APP_API}/nlp/${uuid}/${pageIndex+1}`, {
          method: "get",
        })
          .then((response) => response.json())
          .then((result) => {
            // console.log("Success:", result);
            handleEditPage(result, pageIndex)
          })
          .catch((error) => {
            // console.error("Error:", error);
          });
      }
    },
    page?.status === statuses.ready ? null : 5000
  );

  return (
    <Canvas
      nlpBoxes={page?.boxes?.nlp}
      accuracy={page?.boxes?.value}
      pageNumber={pageIndex+1}
      uuid={uuid}
      pageStatus={page?.status}
    />
  );
}

export default Page;

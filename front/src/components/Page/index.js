import Canvas from "../Canvas";
import { useInterval } from "react-use";
import statuses from "../../constants/statuses";
import Spinner from "../Spinner";
import DownloadPage from "../DownloadPage";

function Page({ uuid, page, pageIndex, handleEditPage, pagesCount }) {
  const { status } = page;
  const boxes = page?.boxes?.nlp;
  const accuracy = page?.boxes?.value;

  const isReady = status === statuses.ready;

  useInterval(
    () => {
      if (uuid) {
        fetch(`${process.env.REACT_APP_API}/nlp/${uuid}/${pageIndex + 1}`, {
          method: "get",
        })
          .then((response) => response.json())
          .then((result) => {
            // console.log("Success:", result);
            handleEditPage(result, pageIndex);
          })
          .catch((error) => {
            // console.error("Error:", error);
          });
      }
    },
    page?.status === statuses.ready ? null : 3000
  );

  function handleEditBoxes(newBoxes) {
    handleEditPage(
      {
        ...page,
        boxes: {
          ...page.boxes,
          nlp: newBoxes,
        },
      },
      pageIndex
    );
  }

  return (
    <div className="flex flex-wrap w-full mt-8">
      <div className="lg:w-4/5 md:w-1/2 md:pr-10">
        <Canvas
          handleEditBoxes={handleEditBoxes}
          pageIndex={pageIndex}
          uuid={uuid}
          pageStatus={status}
        />
      </div>
      <div className="lg:w-1/5 md:w-1/2">
        <h2 className="font-medium title-font text-gray-900 mb-4 text-xl">
          Страница {pageIndex + 1} из {pagesCount}
        </h2>
        <div className="p-4 text-gray-600 mb-8 rounded-lg shadow bg-white">
          Мы постарались отметить закрашенными блоками все ФИО, но система не
          дает 100% результат и вы можете помочь ей научиться отметив слова для
          деперсонификации.
        </div>
        {!isReady ? (
          <div className="p-4 text-gray-600 mt-8 rounded-lg shadow bg-white">
            <Spinner /> Идет распознавание
          </div>
        ) : (
          <>
            <div className="p-4 text-purple-600 mb-8 rounded-lg shadow bg-gradient-to-r from-purple-50 to-purple-100 flex">
              <div className="flex-1 text-xl">
                {Math.round(accuracy * 100)}%
              </div>
              <div className="text-right flex-1">
                <a
                  href="#"
                  title="Уровень уверенности модели в качестве обезличивания"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-6 w-6 inline-block"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                </a>
              </div>
            </div>
            <DownloadPage boxes={boxes} uuid={uuid} pageIndex={pageIndex} />
          </>
        )}
      </div>
    </div>
  );
}

export default Page;

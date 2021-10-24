import { Image, Layer, Stage, Rect } from "react-konva";
import React, { useEffect, useState, useRef } from "react";
import useImage from "use-image";
import { useMeasure } from "react-use";
import DownloadPage from "../DownloadPage";
import statuses from "../../constants/statuses";
import Spinner from "../Spinner";

function downloadURI(uri, name) {
  let link = document.createElement("a");
  link.download = name;
  link.href = uri;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

const TestImage = ({ src }) => {
  const [image] = useImage(src, "Anonymous");
  return <Image image={image} />;
};

function Canvas({ uuid, nlpBoxes, pageNumber, pageStatus, accuracy }) {
  const isObfuscated = pageStatus === statuses.obfuscated;
  const isReady = pageStatus === statuses.ready;
  const inInProgress = pageStatus === statuses.in_progress;
  const [ref, { x, y, width, height, top, right, bottom, left }] = useMeasure();
  const stageRef = useRef(null);
  const [boxes, setBoxes] = useState(nlpBoxes);
  const [stageOptions, setStageOptions] = useState({
    stageScale: 1,
    stageX: 0,
    stageY: 0,
  });

  function removeWord(index) {
    const newBoxes = boxes.map((box, i) => {
      if (index === i) {
        return { ...box, propn: !box?.propn };
      }
      return box;
    });
    setBoxes(newBoxes);
  }

  useEffect(() => {
    setBoxes(nlpBoxes);
  }, [nlpBoxes]);

  function handleWheel(e) {
    e.evt.preventDefault();

    const scaleBy = 1.3;
    const stage = e.target.getStage();
    const oldScale = stage.scaleX();
    const mousePointTo = {
      x: stage.getPointerPosition().x / oldScale - stage.x() / oldScale,
      y: stage.getPointerPosition().y / oldScale - stage.y() / oldScale,
    };

    const newScale = e.evt.deltaY > 0 ? oldScale * scaleBy : oldScale / scaleBy;

    setStageOptions({
      stageScale: newScale,
      stageX:
        -(mousePointTo.x - stage.getPointerPosition().x / newScale) * newScale,
      stageY:
        -(mousePointTo.y - stage.getPointerPosition().y / newScale) * newScale,
    });
  }

  const handleExport = () => {
    stageRef.current.resetZoom();
    const uri = stageRef.current.toDataURL();
    downloadURI(uri, "export.png");
  };

  return (
    <div className="flex flex-wrap w-full mt-8">
      {/*<button className="btn-blue mb-2" onClick={handleExport}>*/}
      {/*  Скачать png*/}
      {/*</button>*/}
      <div className="lg:w-4/5 md:w-1/2 md:pr-10">
        <div
          className="w-full h-screen-half border-gray-500 border-2 rounded-lg overflow-hidden"
          ref={ref}
        >
          <Stage
            draggable
            width={width}
            height={height}
            onWheel={handleWheel}
            scaleX={stageOptions.stageScale}
            scaleY={stageOptions.stageScale}
            x={stageOptions.stageX}
            y={stageOptions.stageY}
            ref={stageRef}
          >
            <Layer>
              {uuid && pageNumber && (
                <TestImage
                  src={`${process.env.REACT_APP_API}/file/${uuid}/${pageNumber}.jpg`}
                />
              )}
              {boxes &&
                boxes.map((box, index) => {
                  if (box?.propn) {
                    return (
                      <Rect
                        onClick={() => removeWord(index)}
                        key={index}
                        x={box?.x}
                        y={box?.y}
                        width={box?.w}
                        height={box?.h}
                        stroke="black"
                        fill="black"
                        opacity={0.5}
                        onMouseEnter={(e) => {
                          // style stage container:
                          const container = e.target.getStage().container();
                          e.target.stroke("red");
                          container.style.cursor = "pointer";
                          container.style.border = "red";
                        }}
                        onMouseLeave={(e) => {
                          const container = e.target.getStage().container();
                          container.style.cursor = "default";
                          e.target.stroke("black");
                        }}
                      />
                    );
                  }
                  return (
                    <Rect
                      onClick={() => removeWord(index)}
                      key={index}
                      x={box?.x}
                      y={box?.y}
                      width={box?.w}
                      height={box?.h}
                      stroke="black"
                      onMouseEnter={(e) => {
                        // style stage container:
                        const container = e.target.getStage().container();
                        e.target.stroke("red");
                        container.style.cursor = "pointer";
                        container.style.border = "red";
                      }}
                      onMouseLeave={(e) => {
                        const container = e.target.getStage().container();
                        container.style.cursor = "default";
                        e.target.stroke("black");
                      }}
                    />
                  );
                })}
            </Layer>
          </Stage>
        </div>
      </div>
      <div className="lg:w-1/5 md:w-1/2">
        <h2 className="font-medium title-font text-gray-900 mb-4 text-xl">
          Страница {pageNumber}
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
            <DownloadPage boxes={boxes} uuid={uuid} pageNumber={pageNumber} />
          </>
        )}
      </div>
    </div>
  );
}

export default Canvas;

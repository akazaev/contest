import { Image, Layer, Stage, Rect } from "react-konva";
import React, { useEffect, useState, useRef, useContext } from "react";
import useImage from "use-image";
import { useMeasure } from "react-use";
import statuses from "../../constants/statuses";
import Annotation from "./Annotation";
import { StateContext } from "../Pages";

const minScale = 0.05;
const maxScale = 20;

function downloadURI(uri, name) {
  let link = document.createElement("a");
  link.download = name;
  link.href = uri;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

const TestImage = ({ src, showAll, onMouseDown }) => {
  const [image, status] = useImage(src, "Anonymous");

  useEffect(() => {
    if (status === "loaded") {
      showAll();
    }
  }, [status]);

  return <Image image={image} onMouseDown={onMouseDown} />;
};

function Canvas({ uuid, pageIndex, pageStatus, handleEditBoxes }) {
  const state = useContext(StateContext);
  const boxes = state[pageIndex]?.boxes?.nlp || [];

  const isObfuscated = pageStatus === statuses.obfuscated;
  const isReady = pageStatus === statuses.ready;
  const inInProgress = pageStatus === statuses.in_progress;
  const [ref, { x, y, width, height, top, right, bottom, left }] = useMeasure();
  const stageRef = useRef(null);
  const layerRef = useRef(null);
  const [selectedIndex, selectAnnotation] = useState(null);
  const [newAnnotation, setNewAnnotation] = useState([]);
  const [stageOptions, setStageOptions] = useState({
    stageScale: 1,
    stageX: 0,
    stageY: 0,
    editMode: false,
    draggable: true,
  });

  function setBoxes(boxes) {
    handleEditBoxes(boxes);
  }

  function deleteBox(index) {
    const newBoxes = boxes.filter((box, i) => i !== index);
    setBoxes(newBoxes);
  }

  function removeWord(index) {
    const { text } = boxes[index];
    const newBoxes = boxes.map((box, i) => {
      if ((text === box?.text && text !== "") || index === i) {
        return { ...box, propn: !box?.propn };
      }
      return box;
    });
    setBoxes(newBoxes);
  }

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

    if (newScale < maxScale && newScale > minScale) {
      setStageOptions({
        ...stageOptions,
        stageScale: newScale,
        stageX:
          -(mousePointTo.x - stage.getPointerPosition().x / newScale) *
          newScale,
        stageY:
          -(mousePointTo.y - stage.getPointerPosition().y / newScale) *
          newScale,
      });
    }
  }

  function changeScale(value) {
    const scale = stageOptions.stageScale + value;
    if (scale < maxScale && scale > minScale) {
      setStageOptions({
        ...stageOptions,
        stageScale: stageOptions.stageScale + value,
      });
    }
  }

  function switchEditMode() {
    selectAnnotation(null);
    setStageOptions({
      ...stageOptions,
      editMode: !stageOptions.editMode,
      draggable: !stageOptions.draggable,
    });
  }

  const showAll = () => {
    const layerBox = layerRef.current.getClientRect({
      relativeTo: stageRef.current,
    });
    // If you need padding on stage
    const padding = 0;
    const scale = Math.min(
      stageRef.current.width() / (layerBox.width + padding * 2),
      stageRef.current.height() / (layerBox.height + padding * 2)
    );
    setStageOptions({
      ...stageOptions,
      stageScale: scale,
      // Fit to center
      stageX: stageRef.current.width() / 2 - (layerBox.width / 2) * scale,
      stageY: -layerBox.y * scale + padding * scale,
      // stageX: -layerBox.x * scale + padding * scale,
      // stageY: -layerBox.y * scale + padding * scale,
    });
  };

  function handleMouseDownStage(event) {
    if (
      selectedIndex === null &&
      newAnnotation.length === 0 &&
      stageOptions.editMode
    ) {
      const stage = event.target.getStage();
      const { x, y } = stage.getPointerPosition();

      const mousePointTo = {
        x: x / stageOptions.stageScale - stage.x() / stageOptions.stageScale,
        y: y / stageOptions.stageScale - stage.y() / stageOptions.stageScale,
      };

      setNewAnnotation([
        {
          x: mousePointTo.x,
          y: mousePointTo.y,
          w: 0,
          h: 0,
          text: "",
          propn: true,
        },
      ]);
    }
  }

  function handleMouseMoveStage(event) {
    if (selectedIndex === null && newAnnotation.length === 1) {
      const sx = newAnnotation[0].x;
      const sy = newAnnotation[0].y;

      const stage = event.target.getStage();
      const { x, y } = stage.getPointerPosition();

      const mousePointTo = {
        x: x / stageOptions.stageScale - stage.x() / stageOptions.stageScale,
        y: y / stageOptions.stageScale - stage.y() / stageOptions.stageScale,
      };

      setNewAnnotation([
        {
          x: sx,
          y: sy,
          w: mousePointTo.x - sx,
          h: mousePointTo.y - sy,
          text: "",
          propn: true,
        },
      ]);
    }
  }

  function handleMouseUpStage() {
    if (selectedIndex === null && newAnnotation.length === 1) {
      if (
        Math.abs(newAnnotation[0].w) > 20 ||
        Math.abs(newAnnotation[0].h) > 20
      ) {
        setBoxes([...boxes, ...newAnnotation]);
      }
      setNewAnnotation([]);
    }
  }

  function handleMouseEnterStage(event) {
    if (stageOptions.editMode) {
      event.target.getStage().container().style.cursor = "crosshair";
    } else {
      event.target.getStage().container().style.cursor = "grab";
    }
  }

  function annotationOnChange(newAttrs, index) {
    const newBoxes = boxes.map((box, i) => {
      if (index === i) {
        return {
          ...box,
          x: newAttrs?.x,
          y: newAttrs?.y,
          w: newAttrs?.width,
          h: newAttrs?.height,
        };
      }
      return box;
    });
    setBoxes(newBoxes);
  }

  function handleKeyDown(event) {
    if (event.keyCode === 8 || event.keyCode === 46) {
      if (selectedIndex !== null) {
        deleteBox(selectedIndex);
      }
    }
  }

  const annotationsToDraw = [...boxes, ...newAnnotation];
  const imageUrl = `${process.env.REACT_APP_API}/file/${uuid}/${
    pageIndex + 1
  }.jpg`;

  return (
    <div
      className="w-full h-screen-half bg-gray-100 border-gray-500 border-2 rounded-lg overflow-hidden relative"
      ref={ref}
      tabIndex={1}
      onKeyDown={handleKeyDown}
    >
      <button
        className={`${
          stageOptions.editMode && "bg-purple-200"
        } btn-white absolute top-40 right-4 z-50`}
        onClick={switchEditMode}
        title="Режим редактирования"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
          />
        </svg>
      </button>
      <button
        className="btn-white absolute top-16 right-4 z-50"
        onClick={() => changeScale(0.1)}
        title="Увеличить маcштаб"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 4v16m8-8H4"
          />
        </svg>
      </button>
      <button
        className={`btn-white absolute top-28 right-4 z-50`}
        onClick={() => changeScale(-0.1)}
        title="Уменьшить маcштаб"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M20 12H4"
          />
        </svg>
      </button>
      <button
        className="btn-white absolute top-4 right-4 z-50"
        onClick={showAll}
        title="Показать всё"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M10 21h7a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v11m0 5l4.879-4.879m0 0a3 3 0 104.243-4.242 3 3 0 00-4.243 4.242z"
          />
        </svg>
      </button>
      <Stage
        draggable={stageOptions.draggable}
        width={width}
        height={height}
        onWheel={handleWheel}
        scaleX={stageOptions.stageScale}
        scaleY={stageOptions.stageScale}
        x={stageOptions.stageX}
        y={stageOptions.stageY}
        ref={stageRef}
        onMouseDown={handleMouseDownStage}
        onMouseMove={handleMouseMoveStage}
        onMouseUp={handleMouseUpStage}
        onMouseEnter={handleMouseEnterStage}
      >
        <Layer ref={layerRef}>
          {imageUrl && (
            <TestImage
              onMouseDown={() => {
                // deselect when clicked on empty area
                selectAnnotation(null);
              }}
              showAll={showAll}
              src={imageUrl}
            />
          )}
          {annotationsToDraw &&
            stageOptions.editMode &&
            annotationsToDraw.map((box, index) => (
              <Annotation
                key={index}
                shapeProps={{
                  x: box?.x,
                  y: box?.y,
                  width: box?.w,
                  height: box?.h,
                }}
                isSelected={index === selectedIndex}
                onSelect={selectAnnotation}
                index={index}
                onChange={annotationOnChange}
              />
            ))}
          {boxes &&
            !stageOptions.editMode &&
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
  );
}

export default Canvas;

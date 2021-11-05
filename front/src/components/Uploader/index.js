import { useState } from "react";
import Spinner from "../Spinner";

function Uploader({ setAppState }) {
  const [selectedFile, setSelectedFile] = useState();
  const [loading, setLoading] = useState(false);
  const [isSelected, setIsSelected] = useState(false);

  const changeHandler = (event) => {
    setSelectedFile(event.target.files[0]);
    setIsSelected(true);
  };

  const handleSubmission = () => {
    const formData = new FormData();

    formData.append("document", selectedFile);
    setLoading(true);
    fetch(`${process.env.REACT_APP_API}/upload`, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((result) => {
        // console.log("Success:", result);
        setLoading(false);
        setAppState((state) => ({ ...state, docUuid: result?.uuid }));
      })
      .catch((error) => {
        setLoading(false);
        // console.error("Error:", error);
      });
  };

  return (
    <div>
      <section className="text-gray-600 body-font">
        <div className="flex flex-wrap w-full">
          <div className="lg:w-2/5 md:w-1/2 md:pr-10 md:py-6">
            <div className="flex relative pb-12">
              <div className="h-full w-10 absolute inset-0 flex items-center justify-center">
                <div className="h-full w-1 bg-gray-200 pointer-events-none" />
              </div>
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-indigo-500 inline-flex items-center justify-center text-white relative z-10">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <div className="flex-grow pl-4">
                <h2 className="font-medium title-font text-sm text-gray-900 mb-1 tracking-wider">
                  ШАГ 1
                </h2>
                {isSelected ? (
                  <>
                    <p className="leading-relaxed mb-2">
                      Имя файла:{" "}
                      <span className="font-semibold">{selectedFile.name}</span>
                    </p>
                    <p className="leading-relaxed mb-2">
                      Размер:{" "}
                      <span className="font-semibold">{selectedFile.size}</span>
                    </p>
                  </>
                ) : (
                  <p className="leading-relaxed mb-2">
                    Выберите файл для загрузки
                  </p>
                )}
                <div className="mt-4">
                  {loading ? (
                    <Spinner />
                  ) : (
                    <>
                      <input
                        className="mr-2"
                        type="file"
                        name="file"
                        onChange={changeHandler}
                      />
                      <button
                        className="lg:mt-0 mt-4 btn-green"
                        onClick={handleSubmission}
                      >
                        Отправить
                      </button>
                    </>
                  )}
                </div>
              </div>
            </div>
            <div className="flex relative pb-12">
              <div className="h-full w-10 absolute inset-0 flex items-center justify-center">
                <div className="h-full w-1 bg-gray-200 pointer-events-none" />
              </div>
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-indigo-500 inline-flex items-center justify-center text-white relative z-10">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <div className="flex-grow pl-4">
                <h2 className="font-medium title-font text-sm text-gray-900 mb-1 tracking-wider">
                  ШАГ 2
                </h2>
                <p className="leading-relaxed">
                  После загрузки происходит преобразования файла в картинки.
                </p>
              </div>
            </div>
            <div className="flex relative pb-12">
              <div className="h-full w-10 absolute inset-0 flex items-center justify-center">
                <div className="h-full w-1 bg-gray-200 pointer-events-none" />
              </div>
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-indigo-500 inline-flex items-center justify-center text-white relative z-10">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"
                  />
                </svg>
              </div>
              <div className="flex-grow pl-4">
                <h2 className="font-medium title-font text-sm text-gray-900 mb-1 tracking-wider">
                  ШАГ 3
                </h2>
                <p className="leading-relaxed">
                  Происходит распознавание текста и определение слов для
                  деперсонификации.
                </p>
              </div>
            </div>
            <div className="flex relative pb-12">
              <div className="h-full w-10 absolute inset-0 flex items-center justify-center">
                <div className="h-full w-1 bg-gray-200 pointer-events-none" />
              </div>
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-indigo-500 inline-flex items-center justify-center text-white relative z-10">
                <svg
                  fill="none"
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  className="w-5 h-5"
                  viewBox="0 0 24 24"
                >
                  <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
              </div>
              <div className="flex-grow pl-4">
                <h2 className="font-medium title-font text-sm text-gray-900 mb-1 tracking-wider">
                  ШАГ 4
                </h2>
                <p className="leading-relaxed">
                  Вы можете отметить дополнительные слова для деперсонификации,
                  либо снять отметку с ошибочных слов.
                </p>
              </div>
            </div>
            <div className="flex relative">
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-indigo-500 inline-flex items-center justify-center text-white relative z-10">
                <svg
                  fill="none"
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  className="w-5 h-5"
                  viewBox="0 0 24 24"
                >
                  <path d="M22 11.08V12a10 10 0 11-5.93-9.14" />
                  <path d="M22 4L12 14.01l-3-3" />
                </svg>
              </div>
              <div className="flex-grow pl-4">
                <h2 className="font-medium title-font text-sm text-gray-900 mb-1 tracking-wider">
                  ФИНИШ
                </h2>
                <p className="leading-relaxed">
                  Выгрузите готовые файлы. Вы великолепны!
                </p>
              </div>
            </div>
          </div>
          <div className="lg:w-3/5 md:w-1/2 object-cover object-center rounded-lg md:mt-0 mt-12">
            <div className="h-full mt-4 p-4 bg-gradient-to-r from-purple-400 via-blue-500 to-indigo-500 rounded-3xl shadow-lg">
              <div className="h-full rounded-3xl overflow-hidden shadow-lg">
                <video
                  autoPlay
                  muted
                  loop
                  controls
                  className="object-cover w-full h-full"
                >
                  <source src={"demo.webm"} type="video/webm" />
                </video>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Uploader;

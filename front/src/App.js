import Uploader from "./components/Uploader";
import { useState } from "react";
import ProgressChecker from "./components/ProgressChecker";
import Pages from "./components/Pages";
import statuses from "./constants/statuses";

function App() {
  const [appState, setAppState] = useState({});

  function clearUuid() {
    setAppState({});
  }

  // console.log(appState);
  return (
    <div className="App">
      <header className="text-gray-600 body-font bg-white shadow">
        <div className="container mx-auto flex flex-wrap p-5 flex-col md:flex-row items-center">
          <a
            href="/"
            className="flex title-font font-medium items-center text-gray-900 mb-4 md:mb-0"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="w-10 h-10 text-white p-2 bg-black rounded-full hover:bg-red-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
              />
            </svg>
            <span className="ml-3 text-xl uppercase">Инкогнито</span>
          </a>
          <nav className="md:ml-auto flex flex-wrap items-center text-base justify-center">
            {/*  <a className="mr-5 hover:text-gray-900">First Link</a>*/}
            {/*  <a className="mr-5 hover:text-gray-900">Second Link</a>*/}
            {/*  <a className="mr-5 hover:text-gray-900">Third Link</a>*/}
            {/*  <a className="mr-5 hover:text-gray-900">Fourth Link</a>*/}
          </nav>
          <button
            onClick={clearUuid}
            className="inline-flex items-center bg-gray-100 border-0 py-1 px-3 focus:outline-none hover:bg-gray-200 rounded text-base mt-4 md:mt-0"
          >
            Загрузить другой документ
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="w-4 h-4 ml-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
          </button>
        </div>
      </header>
      <div className="container mx-auto p-5">
        {appState?.docUuid ? (
          <>
            {appState?.progress?.status === statuses.ready ? (
              <Pages
                pages={appState?.progress?.files}
                uuid={appState?.progress?.uuid}
              />
            ) : (
              <>
                <ProgressChecker
                  uuid={appState?.docUuid}
                  setAppState={setAppState}
                />
                <div>Обработка страниц ещё идет...</div>
              </>
            )}
          </>
        ) : (
          <Uploader setAppState={setAppState} />
        )}
      </div>
    </div>
  );
}

export default App;

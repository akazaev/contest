import Uploader from "./components/Uploader";
import { useState } from "react";
import ProgressChecker from "./components/ProgressChecker";
import Pages from "./components/Pages";

function App() {
  const [appState, setAppState] = useState({
    docUuid: "15b2dd81-2362-414b-9bb2-005aafb2ea0c",
  });

  console.log(appState);
  return (
    <div className="App">
      <header className="text-gray-600 body-font">
        <div className="container mx-auto flex flex-wrap p-5 flex-col md:flex-row items-center">
          <a className="flex title-font font-medium items-center text-gray-900 mb-4 md:mb-0">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              stroke="currentColor"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              className="w-10 h-10 text-white p-2 bg-indigo-500 rounded-full"
              viewBox="0 0 24 24"
            >
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
            </svg>
            <span className="ml-3 text-xl">Classifr</span>
          </a>
          <nav className="md:ml-auto md:mr-auto flex flex-wrap items-center text-base justify-center">
            <a className="mr-5 hover:text-gray-900">First Link</a>
            <a className="mr-5 hover:text-gray-900">Second Link</a>
            <a className="mr-5 hover:text-gray-900">Third Link</a>
            <a className="mr-5 hover:text-gray-900">Fourth Link</a>
          </nav>
        </div>
      </header>
      <div className="container mx-auto p-5">
        {appState?.docUuid ? (
          <>
            <ProgressChecker
              uuid={appState?.docUuid}
              setAppState={setAppState}
            />
            <Pages progress={appState?.progress} />
          </>
        ) : (
          <Uploader setAppState={setAppState} />
        )}
      </div>
    </div>
  );
}

export default App;

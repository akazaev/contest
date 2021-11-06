import React, { useReducer } from "react";
import Page from "../Page";

export const StateContext = React.createContext();
export const DispatchContext = React.createContext();

function reducer(state, action) {
  switch (action.type) {
    case "editPage":
      return state.map((item, index) => {
        if (index !== action.payload.index) {
          // This isn't the item we care about - keep it as-is
          return item;
        }

        // Otherwise, this is the one we want - return an updated value
        return action.payload.newPage;
      });
    default:
      throw new Error();
  }
}

function Pages({ pages = [], uuid }) {
  const [state, dispatch] = useReducer(reducer, pages);

  function handleEditPage(newPage, index) {
    dispatch({ type: "editPage", payload: { newPage, index } });
  }

  return (
    <DispatchContext.Provider value={dispatch}>
      <StateContext.Provider value={state}>
        <div>
          {state.map((page, index) => (
            <Page
              key={`key_page_${index}`}
              uuid={uuid}
              page={page}
              pagesCount={state.length}
              pageIndex={index}
              handleEditPage={handleEditPage}
            />
          ))}
        </div>
      </StateContext.Provider>
    </DispatchContext.Provider>
  );
}

export default Pages;

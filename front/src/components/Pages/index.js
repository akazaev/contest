import { useReducer } from "react";
import Page from "../Page";

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

  console.log("STATE:", state);
  return (
    <div>
      {state.map((page, index) => (
        <Page
          key={index}
          uuid={uuid}
          page={page}
          pageIndex={index}
          handleEditPage={handleEditPage}
        />
      ))}
    </div>
  );
}

export default Pages;

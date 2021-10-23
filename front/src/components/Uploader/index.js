import { useState } from "react";

function Uploader({ setAppState }) {
  const [selectedFile, setSelectedFile] = useState();
  const [isSelected, setIsSelected] = useState(false);

  const changeHandler = (event) => {
    setSelectedFile(event.target.files[0]);
    setIsSelected(true);
  };

  const handleSubmission = () => {
    const formData = new FormData();

    formData.append("document", selectedFile);

    fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((result) => {
        console.log("Success:", result);
        setAppState((state) => ({ ...state, docUuid: result?.uuid }));
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div>
      <input type="file" name="file" onChange={changeHandler} />
      {isSelected ? (
        <div>
          <p>Имя файла: {selectedFile.name}</p>
          <p>Размер: {selectedFile.size}</p>
        </div>
      ) : (
        <p>Выберите файл для загрузки</p>
      )}
      <div>
        <button className="btn-green" onClick={handleSubmission}>
          Отправить
        </button>
      </div>
    </div>
  );
}

export default Uploader;

import Page from '../Page'

function Pages({ progress }) {
  if (progress) {
    return (
      <div>
        {progress?.files.map((page, index) => (
          <Page key={index} uuid={progress?.uuid} page={page} pageNumber={index+1} />
        ))}
      </div>
    );
  }

  return <div>Обработка страниц еще идет</div>;
}

export default Pages;

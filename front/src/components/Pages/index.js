import Page from '../Page'
import statuses from '../../constants/statuses'

function Pages({ progress }) {
  if (progress?.status === statuses.ready) {
    return (
      <div>
        {progress?.files.map((page, index) => (
          <Page key={index} uuid={progress?.uuid} page={page} pageNumber={index+1} />
        ))}
      </div>
    );
  }

  return <div>Обработка страниц еще идет...</div>;
}

export default Pages;

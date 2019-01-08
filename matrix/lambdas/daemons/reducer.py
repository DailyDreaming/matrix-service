from matrix.common import date
from matrix.common.aws.batch_handler import BatchHandler
from matrix.common.constants import MatrixFormat
from matrix.common.logging import Logging
from matrix.common.request.request_cache import RequestCache
from matrix.common.request.request_tracker import RequestTracker, Subtask
from matrix.common.zarr.s3_zarr_store import S3ZarrStore

logger = Logging.get_logger(__name__)


class Reducer:
    def __init__(self, request_id: str, request_hash: str):
        Logging.set_correlation_id(logger, value=request_hash)

        self.request_id = request_id
        self.request_hash = request_hash

        self.request_cache = RequestCache(self.request_id)
        self.request_tracker = RequestTracker(self.request_hash)

        self.batch_handler = BatchHandler(self.request_id, self.request_hash)

    def run(self):
        """
        Write resultant expression matrix zarr metadata in S3 after Workers complete.
        """
        logger.debug(f"Reducer running with parameters: None")

        s3_zarr_store = S3ZarrStore(self.request_hash)
        s3_zarr_store.write_group_metadata()

        if self.request_tracker.format != MatrixFormat.ZARR.value:
            self.batch_handler.schedule_matrix_conversion(self.request_tracker.format)
        else:
            self.request_tracker.complete_request(duration=(date.get_datetime_now() -
                                                            date.to_datetime(self.request_cache.creation_date))
                                                  .total_seconds())

        self.request_tracker.complete_subtask_execution(Subtask.REDUCER)

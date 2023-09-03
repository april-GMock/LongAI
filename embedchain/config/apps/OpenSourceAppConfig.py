from typing import Optional

from .BaseAppConfig import BaseAppConfig


class OpenSourceAppConfig(BaseAppConfig):
    """
    Config to initialize an embedchain custom `OpenSourceApp` instance, with extra config options.
    """

    def __init__(
        self,
        log_level=None,
        id=None,
        collect_metrics: Optional[bool] = None,
        model=None,
        collection_name: Optional[str] = None,
    ):
        """
        :param log_level: Optional. (String) Debug level
        ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'].
        :param id: Optional. ID of the app. Document metadata will have this id.
        :param collect_metrics: Defaults to True. Send anonymous telemetry to improve embedchain.
        :param model: Optional. GPT4ALL uses the model to instantiate the class.
        So unlike `App`, it has to be provided before querying.
        :param collection_name: Optional. Default collection name. It's recommended to use app.set_collection_name() instead.
        """
        self.model = model or "orca-mini-3b.ggmlv3.q4_0.bin"

        super().__init__(
            log_level=log_level,
            id=id,
            collect_metrics=collect_metrics,
            collection_name=collection_name
        )

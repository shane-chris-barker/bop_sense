from bop_common.interfaces.service_starter_interface import ServiceStarterInterface
from bop_common.dtos.service_info_dto import ServiceInfoDTO
from bop_common.enums.service_name import ServiceType
from communication.factories.publisher_factory import get_publisher
from communication.services.voice_publisher_service import VoicePublisherService
from mic.voice_listener import VoiceListener
class MicServiceStarter(ServiceStarterInterface):

    def start(self) -> ServiceInfoDTO:
        voice_publisher = VoicePublisherService(get_publisher())
        listener = VoiceListener(voice_publisher)
        listener.start()
        return ServiceInfoDTO(
            service=ServiceType.VOICE, 
            instance=listener, 
            cleanup_resource=voice_publisher
        )

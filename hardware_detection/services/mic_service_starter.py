from hardware_detection.services.service_starter_interface import ServiceStarterInterface
from hardware_detection.dtos.service_info_dto import ServiceInfoDTO
from hardware_detection.enums.service_name import ServiceType
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

from communication.dtos.communication_dto import CommunicationDTO
from hardware_detection.enums.hardware_type import HardwareType
def test_from_dict_creates_dto_correctly():
    data = {"input":"mic", "content":"Peace and love"}
    dto = CommunicationDTO.from_dict(data)
    assert dto.input == HardwareType.MIC
    assert dto.content ==  "Peace and love"

def test_to_dict_outputs_the_correct_format():
    dto = CommunicationDTO(
        input=HardwareType.CAMERA,
        content="Base64Image"
    )
    result = dto.to_dict()
    assert result == {
        "input": "camera",
        "content": "Base64Image"
    }
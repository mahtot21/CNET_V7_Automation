using CNET_V7_Domain.Domain.SCHEMASchema;
using CNET_V7_Entities.DataModels;
using CNET_V7_Service.Contracts;

namespace CNET_V7_Presentation.BaseControllers.SCHEMASchema;

public class MODEL_NAMEController : BaseController<SAFE_MODEL_NAME, MODEL_NAMEDTO>
{
    public MODEL_NAMEController(IService<SAFE_MODEL_NAME, MODEL_NAMEDTO> commonService) : base(commonService)
    {
    }
}
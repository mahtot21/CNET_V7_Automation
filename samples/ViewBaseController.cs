using CNET_V7_Domain.Domain.SCHEMASchema;
using CNET_V7_Entities.DataModels;
using CNET_V7_Service.Contracts;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CNET_V7_Presentation.BaseControllers.SCHEMASchema;

[Route("api/[controller]")]
[ApiController]
public class MODEL_NAMEController : ControllerBase
{
    private readonly IService<SAFE_MODEL_NAME, MODEL_NAME> _commonService;

    public MODEL_NAMEController(IService<SAFE_MODEL_NAME, MODEL_NAME> commonService)
    {
        _commonService = commonService;
    }

    [HttpGet("filter")]
    public async Task<IActionResult> GetMODEL_NAMEByCondition([FromQuery] Dictionary<string, string> queryParameters)
    {
        var response = await _commonService.FindByConditionView(queryParameters, trackChanges: false);
        if (response.Success)
            return Ok(response.Data);
        return BadRequest(response.Message);
    }
}
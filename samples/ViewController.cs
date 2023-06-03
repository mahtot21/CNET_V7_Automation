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
    private readonly IService<SAFE_MODEL_NAME, MODEL_NAMEDTO> _commonService;

    public MODEL_NAMEController(IService<SAFE_MODEL_NAME, MODEL_NAMEDTO> commonService)
    {
        _commonService = commonService;
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetMODEL_NAMEById(int id)
    {
        var response = await _commonService.FindById(id);
        if (response.Success) return Ok(response.Data);
        return BadRequest(response.Ex.ToString());
    }

    [HttpGet]
    public async Task<IActionResult> GetAllMODEL_NAMEs()
    {
        var response = await _commonService.FindAll(trackChanges: false);
        if(response.Success)
            return Ok(response.Data);
        return BadRequest(response.Message);
    }

    [HttpGet("filter")]
    public async Task<IActionResult> GetMODEL_NAMEByCondition([FromQuery] Dictionary<string, string> queryParameters)
    {
        var response = await _commonService.FindByCondition(queryParameters, trackChanges: false);
        if (response.Success)
            return Ok(response.Data);
        return BadRequest(response.Message);
    }
}
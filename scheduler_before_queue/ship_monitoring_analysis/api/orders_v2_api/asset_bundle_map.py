ASSET_BUNDLE_MAPPING = {
    "PSScene3Band": {
        "assets": {
            "visual": {
                "bundle": "visual"
            },
            "analytic": {
                "bundle": "analytic"
            }
        }
    },
    "SkySatScene": {
        "assets": {
            "ortho_visual": {
                "bundle": "visual"
            }
        }
    }
}

BUNDLE_ASSET_MAPPING = {
    "bundles": {
        "analytic": {
            "name": "Analytic Radiance",
            "description": "Orthorectified product, calibrated to at-sensor radiance",
            "assets": {
                "Landsat8L1G": [
                    "analytic_b1",
                    "analytic_b2",
                    "analytic_b3",
                    "analytic_b4",
                    "analytic_b5",
                    "analytic_b6",
                    "analytic_b7",
                    "analytic_b8",
                    "analytic_b9",
                    "analytic_b10",
                    "analytic_b11",
                    "analytic_bqa",
                    "metadata_txt"
                ],
                "PSOrthoTile": ["analytic", "udm", "analytic_xml"],
                "PSScene3Band": ["analytic", "analytic_xml", "udm"],
                "PSScene4Band": ["analytic", "analytic_xml", "udm"],
                "REOrthoTile": ["analytic", "analytic_xml", "udm"],
                "REScene": [
                    "basic_analytic_b1",
                    "basic_analytic_b2",
                    "basic_analytic_b3",
                    "basic_analytic_b4",
                    "basic_analytic_b5",
                    "basic_analytic_xml",
                    "basic_analytic_rpc",
                    "basic_udm",
                    "basic_analytic_sci",
                    "browse"
                ],
                "Sentinel1": ["ortho_analytic_vv", "ortho_analytic_vh"],
                "Sentinel2L1C": [
                    "analytic_b1",
                    "analytic_b2",
                    "analytic_b3",
                    "analytic_b4",
                    "analytic_b5",
                    "analytic_b6",
                    "analytic_b7",
                    "analytic_b8",
                    "analytic_b8a",
                    "analytic_b9",
                    "analytic_b10",
                    "analytic_b11",
                    "analytic_b12",
                    "metadata_aux"
                ],
                "SkySatScene": ["analytic"]
            }
        },
        "analytic_udm2": {
            "name": "Analytic Radiance with UDM2",
            "description": "Orthorectified product, calibrated to at-sensor radiance. Includes udm2.",
            "assets": {
                "PSOrthoTile": ["analytic", "udm", "udm2", "analytic_xml"],
                "PSScene4Band": ["analytic", "analytic_xml", "udm", "udm2"]
            }
        },
        "analytic_dn": {
            "name": "Uncalibrated DN",
            "description": "This product bundle is deprecated, please use 'uncalibrated_dn' instead",
            "assets": {
                "PSOrthoTile": ["analytic_dn", "analytic_dn_xml", "udm"],
                "PSScene3Band": ["analytic_dn", "analytic_dn_xml", "udm"],
                "PSScene4Band": ["analytic_dn", "analytic_dn_xml", "udm"]
            }
        },
        "analytic_nitf": {
            "name": "Non-Orthorectified Analytic Radiance NITF",
            "description": "This product bundle is deprecated, please use 'basic_analytic_nitf' instead",
            "assets": {
                "REScene": [
                    "basic_analytic_b1_nitf",
                    "basic_analytic_b2_nitf",
                    "basic_analytic_b3_nitf",
                    "basic_analytic_b4_nitf",
                    "basic_analytic_b5_nitf",
                    "basic_analytic_rpc",
                    "basic_analytic_sci",
                    "basic_analytic_xml_nitf",
                    "basic_udm",
                    "browse"
                ]
            }
        },
        "visual": {
            "name": "Visual",
            "description": "Orthorectified product, visually enhanced for optimal appearance",
            "assets": {
                "Landsat8L1G": ["visual"],
                "PSOrthoTile": ["visual", "visual_xml"],
                "PSScene3Band": ["visual", "visual_xml"],
                "REOrthoTile": ["visual", "visual_xml"],
                "Sentinel2L1C": ["visual"],
                "SkySatCollect": ["ortho_visual"],
                "SkySatScene": ["ortho_visual"]
            }
        },
        "uncalibrated_dn": {
            "name": "Uncalibrated DN",
            "description": "Orthorectified product, non-radiometrically-calibrated, raw digital number",
            "assets": {
                "PSOrthoTile": ["analytic_dn", "udm", "analytic_dn_xml"],
                "PSScene3Band": ["analytic_dn", "analytic_dn_xml", "udm"],
                "PSScene4Band": ["analytic_dn", "analytic_dn_xml", "udm"],
                "SkySatCollect": ["ortho_analytic_dn", "ortho_analytic_udm"],
                "SkySatScene": ["ortho_analytic_dn", "ortho_analytic_udm"]
            }
        },
        "uncalibrated_dn_udm2": {
            "name": "Uncalibrated DN with UDM2",
            "description": "Orthorectified product, non-radiometrically-calibrated, raw digital number. Includes udm2.",
            "assets": {
                "PSOrthoTile": ["analytic_dn", "analytic_dn_xml", "udm", "udm2"],
                "PSScene4Band": ["analytic_dn", "analytic_dn_xml", "udm", "udm2"]
            }
        },
        "basic_analytic": {
            "name": "Non-Orthorectified Analytic Radiance",
            "description": "Non-orthorectified, calibrated to at-sensor radiance",
            "assets": {
                "PSScene3Band": [
                    "basic_analytic",
                    "basic_udm",
                    "basic_analytic_rpc",
                    "basic_analytic_xml"
                ],
                "PSScene4Band": [
                    "basic_analytic",
                    "basic_udm",
                    "basic_analytic_rpc",
                    "basic_analytic_xml"
                ],
                "REScene": [
                    "basic_analytic_b1",
                    "basic_analytic_b2",
                    "basic_analytic_b3",
                    "basic_analytic_b4",
                    "basic_analytic_b5",
                    "basic_analytic_xml",
                    "basic_analytic_rpc",
                    "basic_udm",
                    "basic_analytic_sci",
                    "browse"
                ]
            }
        },
        "basic_analytic_udm2": {
            "name": "Non-Orthorectified Analytic Radiance with UDM2",
            "description": "Non-orthorectified, calibrated to at-sensor radiance. Includes udm2.",
            "assets": {
                "PSScene4Band": [
                    "basic_analytic",
                    "basic_udm",
                    "basic_udm2",
                    "basic_analytic_rpc",
                    "basic_analytic_xml"
                ]
            }
        },
        "basic_analytic_dn": {
            "name": "Non-Orthorectified, Uncalibrated DN",
            "description": "This product bundle is deprecated, please use 'basic_uncalibrated_dn' instead",
            "assets": {
                "PSScene3Band": [
                    "basic_analytic_dn",
                    "basic_analytic_dn_rpc",
                    "basic_analytic_dn_xml",
                    "basic_udm"
                ],
                "PSScene4Band": [
                    "basic_analytic_dn",
                    "basic_analytic_dn_xml",
                    "basic_analytic_rpc",
                    "basic_udm"
                ],
                "SkySatScene": ["basic_analytic_dn", "basic_analytic_dn_rpc"]
            }
        },
        "basic_analytic_dn_nitf": {
            "name": "Non-Orthorectified, Uncalibrated DN NITF",
            "description": "This product bundle is deprecated, please use 'basic_uncalibrated_dn_nitf' instead",
            "assets": {
                "PSScene4Band": [
                    "basic_analytic_dn_nitf",
                    "basic_analytic_dn_rpc_nitf",
                    "basic_analytic_dn_xml_nitf",
                    "basic_udm"
                ]
            }
        },
        "basic_uncalibrated_dn": {
            "name": "Non-Orthorectified, Uncalibrated DN",
            "description": "Non-orthorectified, non-radiometrically-calibrated, raw digital number",
            "assets": {
                "PSScene3Band": [
                    "basic_analytic_dn",
                    "basic_analytic_dn_xml",
                    "basic_udm",
                    "basic_analytic_dn_rpc"
                ],
                "PSScene4Band": [
                    "basic_analytic_dn",
                    "basic_analytic_dn_xml",
                    "basic_udm",
                    "basic_analytic_rpc"
                ],
                "SkySatScene": ["basic_analytic_dn", "basic_analytic_dn_rpc"]
            }
        },
        "basic_uncalibrated_dn_udm2": {
            "name": "Non-Orthorectified, Uncalibrated DN with UDM2",
            "description": "Non-orthorectified, non-radiometrically-calibrated, raw digital number. Includes udm2.",
            "assets": {
                "PSScene4Band": [
                    "basic_analytic_dn",
                    "basic_analytic_dn_xml",
                    "basic_udm",
                    "basic_udm2",
                    "basic_analytic_rpc"
                ]
            }
        },
        "analytic_sr": {
            "name": "Analytic Surface Reflectance",
            "description": "Orthorectified product, radiometrically calibrated and atmospherically corrected to surface reflectance",
            "assets": {
                "PSScene4Band": ["analytic_sr", "udm", "analytic_xml"],
                "MOD09GQ": [
                    "analytic_num_observations",
                    "analytic_orbit_pnt",
                    "analytic_granule_pnt",
                    "analytic_sur_refl_b01",
                    "analytic_sur_refl_b02",
                    "analytic_qc_250m",
                    "analytic_obscov",
                    "analytic_iobs_res"
                ],
                "MYD09GQ": [
                    "analytic_num_observations",
                    "analytic_orbit_pnt",
                    "analytic_granule_pnt",
                    "analytic_sur_refl_b01",
                    "analytic_sur_refl_b02",
                    "analytic_qc_250m",
                    "analytic_obscov",
                    "analytic_iobs_res"
                ],
                "MOD09GA": [
                    "analytic_num_observations_500m",
                    "analytic_num_observations_1km",
                    "analytic_state_1km",
                    "analytic_sensor_zenith",
                    "analytic_sensor_azimuth",
                    "analytic_range",
                    "analytic_solar_zenith",
                    "analytic_solar_azimuth",
                    "analytic_gflags",
                    "analytic_orbit_pnt",
                    "analytic_granule_pnt",
                    "analytic_sur_refl_b01",
                    "analytic_sur_refl_b02",
                    "analytic_sur_refl_b03",
                    "analytic_sur_refl_b04",
                    "analytic_sur_refl_b05",
                    "analytic_sur_refl_b06",
                    "analytic_sur_refl_b07",
                    "analytic_qc_500m",
                    "analytic_obscov_500m",
                    "analytic_iobs_res",
                    "analytic_q_scan"
                ],
                "MYD09GA": [
                    "analytic_num_observations_500m",
                    "analytic_num_observations_1km",
                    "analytic_state_1km",
                    "analytic_sensor_zenith",
                    "analytic_sensor_azimuth",
                    "analytic_range",
                    "analytic_solar_zenith",
                    "analytic_solar_azimuth",
                    "analytic_gflags",
                    "analytic_orbit_pnt",
                    "analytic_granule_pnt",
                    "analytic_sur_refl_b01",
                    "analytic_sur_refl_b02",
                    "analytic_sur_refl_b03",
                    "analytic_sur_refl_b04",
                    "analytic_sur_refl_b05",
                    "analytic_sur_refl_b06",
                    "analytic_sur_refl_b07",
                    "analytic_qc_500m",
                    "analytic_obscov_500m",
                    "analytic_iobs_res",
                    "analytic_q_scan"
                ]
            }
        },
        "analytic_sr_udm2": {
            "name": "Analytic Surface Reflectance with UDM2",
            "description": "Orthorectified product, radiometrically calibrated and atmospherically corrected to surface reflectance. Includes udm2.",
            "assets": {
                "PSScene4Band": ["analytic_sr", "analytic_xml", "udm", "udm2"]
            }
        },
        "basic_uncalibrated_dn_nitf": {
            "name": "Non-Orthorectified, Uncalibrated DN NITF",
            "description": "Non-orthorectified, non-radiometrically-calibrated, raw digital number in NITF format",
            "assets": {
                "PSScene4Band": [
                    "basic_analytic_dn_nitf",
                    "basic_analytic_dn_xml_nitf",
                    "basic_analytic_dn_rpc_nitf",
                    "basic_udm"
                ]
            }
        },
        "basic_uncalibrated_dn_nitf_udm2": {
            "name": "Non-Orthorectified, Uncalibrated DN NITF with UDM2",
            "description": "Non-orthorectified, non-radiometrically-calibrated, raw digital number in NITF format. Includes udm2.",
            "assets": {
                "PSScene4Band": [
                    "basic_analytic_dn_nitf",
                    "basic_analytic_dn_xml_nitf",
                    "basic_analytic_dn_rpc_nitf",
                    "basic_udm",
                    "basic_udm2"
                ]
            }
        },
        "basic_analytic_nitf": {
            "name": "Non-Orthorectified Analytic Radiance NITF",
            "description": "Non-orthorectified, calibrated to at-sensor radiance, in NITF format",
            "assets": {
                "PSScene4Band": [
                    "basic_analytic_nitf",
                    "basic_analytic_rpc_nitf",
                    "basic_analytic_xml_nitf",
                    "basic_udm"
                ],
                "REScene": [
                    "basic_analytic_b1_nitf",
                    "basic_analytic_b2_nitf",
                    "basic_analytic_b3_nitf",
                    "basic_analytic_b4_nitf",
                    "basic_analytic_b5_nitf",
                    "basic_analytic_xml_nitf",
                    "basic_analytic_rpc",
                    "basic_udm",
                    "basic_analytic_sci",
                    "browse"
                ]
            }
        },
        "basic_analytic_nitf_udm2": {
            "name": "Non-Orthorectified Analytic Radiance NITF with UDM2",
            "description": "Non-orthorectified, calibrated to at-sensor radiance, in NITF format. Includes udm2.",
            "assets": {
                "PSScene4Band": [
                    "basic_analytic_nitf",
                    "basic_analytic_rpc_nitf",
                    "basic_analytic_xml_nitf",
                    "basic_udm",
                    "basic_udm2"
                ]
            }
        },
        "basic_panchromatic_dn": {
            "name": "Non-Orthorectified, Uncalibrated DN",
            "description": "Unorthorectified panchromatic imagery, non-radiometrically calibrated, raw digital number",
            "assets": {
                "SkySatScene": ["basic_panchromatic_dn", "basic_panchromatic_dn_rpc"]
            }
        },
        "ortho_analytic_dn": {
            "name": "Uncalibrated DN",
            "description": "This product bundle is deprecated, please use 'uncalibrated_dn' instead",
            "assets": {
                "SkySatScene": ["ortho_analytic_dn", "ortho_analytic_udm"]
            }
        },
        "ortho_panchromatic_dn": {
            "name": "Panchromatic DN",
            "description": "This product bundle is deprecated, please use 'panchromatic_dn' instead",
            "assets": {
                "SkySatScene": ["ortho_panchromatic_dn", "ortho_panchromatic_udm"]
            }
        },
        "ortho_pansharpened": {
            "name": "Pansharpened",
            "description": "This product bundle is deprecated, please use 'pansharpened' instead",
            "assets": {
                "SkySatScene": ["ortho_pansharpened", "ortho_pansharpened_udm"]
            }
        },
        "ortho_visual": {
            "name": "Visual",
            "description": "This product bundle is deprecated, please use 'visual' instead",
            "assets": {
                "SkySatScene": ["ortho_analytic_udm", "ortho_visual"]
            }
        },
        "panchromatic_dn": {
            "name": "Panchromatic DN",
            "description": "Orthorectified panchromatic imagery, non-radiometrically calibrated, raw digital number",
            "assets": {
                "SkySatCollect": ["ortho_panchromatic_dn", "ortho_panchromatic_udm"],
                "SkySatScene": ["ortho_panchromatic_dn", "ortho_panchromatic_udm"]
            }
        },
        "pansharpened": {
            "name": "Pansharpened",
            "description": "Orthorectifed, pan-sharpened imagery, non-radiometrically calibrated, raw digital number",
            "assets": {
                "SkySatCollect": ["ortho_pansharpened", "ortho_pansharpened_udm"],
                "SkySatScene": ["ortho_pansharpened", "ortho_pansharpened_udm"]
            }
        },
        "analytic_without_metadata": {
            "name": "Analytic Radiance",
            "description": "Metadata removal per DAS",
            "assets": {
                "Landsat8L1G": [
                    "analytic_b1",
                    "analytic_b2",
                    "analytic_b3",
                    "analytic_b4",
                    "analytic_b5",
                    "analytic_b6",
                    "analytic_b7",
                    "analytic_b8",
                    "analytic_b9",
                    "analytic_b10",
                    "analytic_b11",
                    "analytic_bqa",
                    "metadata_txt"
                ],
                "PSOrthoTile": ["analytic", "udm", "analytic_xml"],
                "PSScene3Band": ["analytic", "analytic_xml", "udm"],
                "PSScene4Band": ["analytic", "analytic_xml", "udm"],
                "REOrthoTile": ["analytic", "analytic_xml", "udm"],
                "REScene": [
                    "basic_analytic_b1",
                    "basic_analytic_b2",
                    "basic_analytic_b3",
                    "basic_analytic_b4",
                    "basic_analytic_b5",
                    "basic_analytic_xml",
                    "basic_analytic_rpc",
                    "basic_udm",
                    "basic_analytic_sci",
                    "browse"
                ],
                "Sentinel1": ["ortho_analytic_vv", "ortho_analytic_vh"],
                "Sentinel2L1C": [
                    "analytic_b1",
                    "analytic_b2",
                    "analytic_b3",
                    "analytic_b4",
                    "analytic_b5",
                    "analytic_b6",
                    "analytic_b7",
                    "analytic_b8",
                    "analytic_b8a",
                    "analytic_b9",
                    "analytic_b10",
                    "analytic_b11",
                    "analytic_b12",
                    "metadata_aux"
                ],
                "SkySatScene": ["analytic"]
            }
        },
        "basic_analytic_without_metadata": {
            "name": "Non-Orthorectified Analytic Radiance - no metadata workaround",
            "description": "Metadata removal per DAS",
            "assets": {
                "PSScene3Band": [
                    "basic_analytic",
                    "basic_udm",
                    "basic_analytic_rpc",
                    "basic_analytic_xml"
                ],
                "PSScene4Band": [
                    "basic_analytic",
                    "basic_udm",
                    "basic_analytic_rpc",
                    "basic_analytic_xml"
                ],
                "REScene": [
                    "basic_analytic_b1",
                    "basic_analytic_b2",
                    "basic_analytic_b3",
                    "basic_analytic_b4",
                    "basic_analytic_b5",
                    "basic_analytic_xml",
                    "basic_analytic_rpc",
                    "basic_udm",
                    "basic_analytic_sci",
                    "browse"
                ]
            }
        },
        "visual_without_metadata": {
            "name": "Visual without metadata",
            "description": "Orthorectified product, visually enhanced for optimal appearance",
            "assets": {
                "Landsat8L1G": ["visual"],
                "PSOrthoTile": ["visual", "visual_xml"],
                "PSScene3Band": ["visual", "visual_xml"],
                "REOrthoTile": ["visual", "visual_xml"],
                "Sentinel2L1C": ["visual"],
                "SkySatCollect": ["ortho_visual", "ortho_analytic_udm"],
                "SkySatScene": ["ortho_visual", "ortho_analytic_udm"]
            }
        },
        "all": {
            "name": "All assets",
            "description": "All assets that can be produced for an item",
            "assets": {
                "Landsat8L1G": [
                    "analytic_b1",
                    "analytic_b2",
                    "analytic_b3",
                    "analytic_b4",
                    "analytic_b5",
                    "analytic_b6",
                    "analytic_b7",
                    "analytic_b8",
                    "analytic_b9",
                    "analytic_b10",
                    "analytic_b11",
                    "analytic_bqa",
                    "metadata_txt",
                    "visual"
                ],
                "MOD09GA": [
                    "analytic_num_observations_500m",
                    "analytic_num_observations_1km",
                    "analytic_state_1km",
                    "analytic_sensor_zenith",
                    "analytic_sensor_azimuth",
                    "analytic_range",
                    "analytic_solar_zenith",
                    "analytic_solar_azimuth",
                    "analytic_gflags",
                    "analytic_orbit_pnt",
                    "analytic_granule_pnt",
                    "analytic_sur_refl_b01",
                    "analytic_sur_refl_b02",
                    "analytic_sur_refl_b03",
                    "analytic_sur_refl_b04",
                    "analytic_sur_refl_b05",
                    "analytic_sur_refl_b06",
                    "analytic_sur_refl_b07",
                    "analytic_qc_500m",
                    "analytic_obscov_500m",
                    "analytic_iobs_res",
                    "analytic_q_scan"
                ],
                "MOD09GQ": [
                    "analytic_num_observations",
                    "analytic_orbit_pnt",
                    "analytic_granule_pnt",
                    "analytic_sur_refl_b01",
                    "analytic_sur_refl_b02",
                    "analytic_qc_250m",
                    "analytic_obscov",
                    "analytic_iobs_res"
                ],
                "MYD09GA": [
                    "analytic_num_observations_500m",
                    "analytic_num_observations_1km",
                    "analytic_state_1km",
                    "analytic_sensor_zenith",
                    "analytic_sensor_azimuth",
                    "analytic_range",
                    "analytic_solar_zenith",
                    "analytic_solar_azimuth",
                    "analytic_gflags",
                    "analytic_orbit_pnt",
                    "analytic_granule_pnt",
                    "analytic_sur_refl_b01",
                    "analytic_sur_refl_b02",
                    "analytic_sur_refl_b03",
                    "analytic_sur_refl_b04",
                    "analytic_sur_refl_b05",
                    "analytic_sur_refl_b06",
                    "analytic_sur_refl_b07",
                    "analytic_qc_500m",
                    "analytic_obscov_500m",
                    "analytic_iobs_res",
                    "analytic_q_scan"
                ],
                "MYD09GQ": [
                    "analytic_num_observations",
                    "analytic_orbit_pnt",
                    "analytic_granule_pnt",
                    "analytic_sur_refl_b01",
                    "analytic_sur_refl_b02",
                    "analytic_qc_250m",
                    "analytic_obscov",
                    "analytic_iobs_res"
                ],
                "PSOrthoTile": [
                    "analytic_dn",
                    "analytic_dn_xml",
                    "udm",
                    "analytic",
                    "analytic_xml",
                    "visual",
                    "visual_xml"
                ],
                "PSScene3Band": [
                    "analytic_dn",
                    "analytic_dn_xml",
                    "udm",
                    "analytic",
                    "analytic_xml",
                    "basic_analytic",
                    "basic_udm",
                    "basic_analytic_rpc",
                    "basic_analytic_xml",
                    "visual",
                    "visual_xml",
                    "basic_analytic_dn",
                    "basic_analytic_dn_rpc",
                    "basic_analytic_dn_xml"
                ],
                "PSScene4Band": [
                    "basic_udm",
                    "analytic_dn",
                    "analytic_dn_xml",
                    "udm",
                    "analytic",
                    "analytic_xml",
                    "basic_analytic",
                    "basic_analytic_rpc",
                    "basic_analytic_xml",
                    "basic_analytic_dn",
                    "basic_analytic_dn_xml",
                    "analytic_sr"
                ],
                "REOrthoTile": [
                    "analytic",
                    "analytic_xml",
                    "udm",
                    "visual",
                    "visual_xml"
                ],
                "REScene": [
                    "basic_analytic_rpc",
                    "basic_udm",
                    "basic_analytic_sci",
                    "browse",
                    "basic_analytic_b1",
                    "basic_analytic_b2",
                    "basic_analytic_b3",
                    "basic_analytic_b4",
                    "basic_analytic_b5",
                    "basic_analytic_xml"
                ],
                "Sentinel1": ["ortho_analytic_vv", "ortho_analytic_vh"],
                "Sentinel2L1C": [
                    "analytic_b1",
                    "analytic_b2",
                    "analytic_b3",
                    "analytic_b4",
                    "analytic_b5",
                    "analytic_b6",
                    "analytic_b7",
                    "analytic_b8",
                    "analytic_b8a",
                    "analytic_b9",
                    "analytic_b10",
                    "analytic_b11",
                    "analytic_b12",
                    "metadata_aux",
                    "visual"
                ],
                "SkySatCollect": [
                    "ortho_analytic_dn",
                    "ortho_analytic_udm",
                    "ortho_panchromatic_dn",
                    "ortho_panchromatic_udm",
                    "ortho_visual",
                    "ortho_pansharpened",
                    "ortho_pansharpened_udm"
                ],
                "SkySatScene": [
                    "ortho_analytic_udm",
                    "ortho_visual",
                    "analytic",
                    "ortho_analytic_dn",
                    "ortho_panchromatic_dn",
                    "ortho_panchromatic_udm",
                    "basic_panchromatic_dn",
                    "basic_panchromatic_dn_rpc",
                    "basic_analytic_dn",
                    "basic_analytic_dn_rpc",
                    "ortho_pansharpened",
                    "ortho_pansharpened_udm"
                ]
            }
        },
        "all_udm2": {
            "name": "All assets with UDM2",
            "description": "All assets that can be produced for an item. Includes udm2.",
            "assets": {
                "PSOrthoTile": [
                    "analytic_dn",
                    "analytic_dn_xml",
                    "udm",
                    "udm2",
                    "analytic",
                    "analytic_xml",
                    "visual",
                    "visual_xml"
                ],
                "PSScene4Band": [
                    "basic_udm",
                    "basic_udm2",
                    "analytic_dn",
                    "analytic_dn_xml",
                    "udm",
                    "udm2",
                    "analytic",
                    "analytic_xml",
                    "basic_analytic",
                    "basic_analytic_rpc",
                    "basic_analytic_xml",
                    "basic_analytic_dn",
                    "basic_analytic_dn_xml",
                    "analytic_sr"
                ]
            }
        }
    },
    "deprecated": {
        "analytic": {
            "assets": {
                "REScene": [
                    "basic_analytic_b1",
                    "basic_analytic_b2",
                    "basic_analytic_b3",
                    "basic_analytic_b4",
                    "basic_analytic_b5",
                    "basic_analytic_xml",
                    "basic_analytic_rpc",
                    "basic_udm",
                    "basic_analytic_sci",
                    "browse"
                ]
            }
        },
        "analytic_dn": {
            "assets": {
                "PSOrthoTile": ["analytic_dn", "analytic_dn_xml", "udm"],
                "PSScene3Band": ["analytic_dn", "analytic_dn_xml", "udm"],
                "PSScene4Band": ["analytic_dn", "analytic_dn_xml", "udm"]
            }
        },
        "analytic_nitf": {
            "assets": {
                "REScene": [
                    "basic_analytic_b1_nitf",
                    "basic_analytic_b2_nitf",
                    "basic_analytic_b3_nitf",
                    "basic_analytic_b4_nitf",
                    "basic_analytic_b5_nitf",
                    "basic_analytic_rpc",
                    "basic_analytic_sci",
                    "basic_analytic_xml_nitf",
                    "basic_udm",
                    "browse"
                ]
            }
        },
        "basic_analytic_dn": {
            "assets": {
                "PSScene3Band": [
                    "basic_analytic_dn",
                    "basic_analytic_dn_rpc",
                    "basic_analytic_dn_xml",
                    "basic_udm"
                ],
                "PSScene4Band": [
                    "basic_analytic_dn",
                    "basic_analytic_dn_xml",
                    "basic_analytic_rpc",
                    "basic_udm"
                ],
                "SkySatScene": ["basic_analytic_dn", "basic_analytic_dn_rpc"]
            }
        },
        "basic_analytic_dn_nitf": {
            "assets": {
                "PSScene4Band": [
                    "basic_analytic_dn_nitf",
                    "basic_analytic_dn_rpc_nitf",
                    "basic_analytic_dn_xml_nitf",
                    "basic_udm"
                ]
            }
        },
        "ortho_analytic_dn": {
            "assets": {
                "SkySatScene": ["ortho_analytic_dn", "ortho_analytic_udm"]
            }
        },
        "ortho_panchromatic_dn": {
            "assets": {
                "SkySatScene": ["ortho_panchromatic_dn", "ortho_panchromatic_udm"]
            }
        },
        "ortho_pansharpened": {
            "assets": {
                "SkySatScene": ["ortho_pansharpened", "ortho_pansharpened_udm"]
            }
        },
        "ortho_visual": {
            "assets": {
                "SkySatScene": ["ortho_analytic_udm", "ortho_visual"]
            }
        }
    },
    "version": "2019-03-08"
}

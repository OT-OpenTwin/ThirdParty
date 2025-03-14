// Copyright 2022 The Tint Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

////////////////////////////////////////////////////////////////////////////////
// File generated by tools/src/cmd/gen
// using the template:
//   src/tint/builtin/builtin_test.cc.tmpl
//
// Do not modify this file directly
////////////////////////////////////////////////////////////////////////////////

#include "src/tint/builtin/builtin.h"

#include <string>

#include "gtest/gtest.h"

#include "src/tint/utils/string.h"

namespace tint::builtin {
namespace {

namespace parse_print_tests {

struct Case {
    const char* string;
    Builtin value;
};

inline std::ostream& operator<<(std::ostream& out, Case c) {
    return out << "'" << std::string(c.string) << "'";
}

static constexpr Case kValidCases[] = {
    {"array", Builtin::kArray},
    {"atomic", Builtin::kAtomic},
    {"bool", Builtin::kBool},
    {"f16", Builtin::kF16},
    {"f32", Builtin::kF32},
    {"i32", Builtin::kI32},
    {"mat2x2", Builtin::kMat2X2},
    {"mat2x2f", Builtin::kMat2X2F},
    {"mat2x2h", Builtin::kMat2X2H},
    {"mat2x3", Builtin::kMat2X3},
    {"mat2x3f", Builtin::kMat2X3F},
    {"mat2x3h", Builtin::kMat2X3H},
    {"mat2x4", Builtin::kMat2X4},
    {"mat2x4f", Builtin::kMat2X4F},
    {"mat2x4h", Builtin::kMat2X4H},
    {"mat3x2", Builtin::kMat3X2},
    {"mat3x2f", Builtin::kMat3X2F},
    {"mat3x2h", Builtin::kMat3X2H},
    {"mat3x3", Builtin::kMat3X3},
    {"mat3x3f", Builtin::kMat3X3F},
    {"mat3x3h", Builtin::kMat3X3H},
    {"mat3x4", Builtin::kMat3X4},
    {"mat3x4f", Builtin::kMat3X4F},
    {"mat3x4h", Builtin::kMat3X4H},
    {"mat4x2", Builtin::kMat4X2},
    {"mat4x2f", Builtin::kMat4X2F},
    {"mat4x2h", Builtin::kMat4X2H},
    {"mat4x3", Builtin::kMat4X3},
    {"mat4x3f", Builtin::kMat4X3F},
    {"mat4x3h", Builtin::kMat4X3H},
    {"mat4x4", Builtin::kMat4X4},
    {"mat4x4f", Builtin::kMat4X4F},
    {"mat4x4h", Builtin::kMat4X4H},
    {"ptr", Builtin::kPtr},
    {"sampler", Builtin::kSampler},
    {"sampler_comparison", Builtin::kSamplerComparison},
    {"texture_1d", Builtin::kTexture1D},
    {"texture_2d", Builtin::kTexture2D},
    {"texture_2d_array", Builtin::kTexture2DArray},
    {"texture_3d", Builtin::kTexture3D},
    {"texture_cube", Builtin::kTextureCube},
    {"texture_cube_array", Builtin::kTextureCubeArray},
    {"texture_depth_2d", Builtin::kTextureDepth2D},
    {"texture_depth_2d_array", Builtin::kTextureDepth2DArray},
    {"texture_depth_cube", Builtin::kTextureDepthCube},
    {"texture_depth_cube_array", Builtin::kTextureDepthCubeArray},
    {"texture_depth_multisampled_2d", Builtin::kTextureDepthMultisampled2D},
    {"texture_external", Builtin::kTextureExternal},
    {"texture_multisampled_2d", Builtin::kTextureMultisampled2D},
    {"texture_storage_1d", Builtin::kTextureStorage1D},
    {"texture_storage_2d", Builtin::kTextureStorage2D},
    {"texture_storage_2d_array", Builtin::kTextureStorage2DArray},
    {"texture_storage_3d", Builtin::kTextureStorage3D},
    {"u32", Builtin::kU32},
    {"vec2", Builtin::kVec2},
    {"vec2f", Builtin::kVec2F},
    {"vec2h", Builtin::kVec2H},
    {"vec2i", Builtin::kVec2I},
    {"vec2u", Builtin::kVec2U},
    {"vec3", Builtin::kVec3},
    {"vec3f", Builtin::kVec3F},
    {"vec3h", Builtin::kVec3H},
    {"vec3i", Builtin::kVec3I},
    {"vec3u", Builtin::kVec3U},
    {"vec4", Builtin::kVec4},
    {"vec4f", Builtin::kVec4F},
    {"vec4h", Builtin::kVec4H},
    {"vec4i", Builtin::kVec4I},
    {"vec4u", Builtin::kVec4U},
};

static constexpr Case kInvalidCases[] = {
    {"arccy", Builtin::kUndefined},
    {"3a", Builtin::kUndefined},
    {"aVray", Builtin::kUndefined},
    {"1tomic", Builtin::kUndefined},
    {"aoqqic", Builtin::kUndefined},
    {"atomll77", Builtin::kUndefined},
    {"ppqooH", Builtin::kUndefined},
    {"c", Builtin::kUndefined},
    {"bGo", Builtin::kUndefined},
    {"f1vi", Builtin::kUndefined},
    {"f8WW", Builtin::kUndefined},
    {"fxx", Builtin::kUndefined},
    {"fgg", Builtin::kUndefined},
    {"X", Builtin::kUndefined},
    {"332", Builtin::kUndefined},
    {"iE2", Builtin::kUndefined},
    {"iPTT", Builtin::kUndefined},
    {"dxx2", Builtin::kUndefined},
    {"44at2x2", Builtin::kUndefined},
    {"mSSVV2x2", Builtin::kUndefined},
    {"mat2R2", Builtin::kUndefined},
    {"mF2x9f", Builtin::kUndefined},
    {"matx2f", Builtin::kUndefined},
    {"VOORRH2f", Builtin::kUndefined},
    {"ma2xyh", Builtin::kUndefined},
    {"llnarr2772h", Builtin::kUndefined},
    {"mat24200", Builtin::kUndefined},
    {"m2oo", Builtin::kUndefined},
    {"atzz3", Builtin::kUndefined},
    {"1it2xpp", Builtin::kUndefined},
    {"mat2xXXf", Builtin::kUndefined},
    {"9II5ann2x3f", Builtin::kUndefined},
    {"mataSSrHHYf", Builtin::kUndefined},
    {"makkh", Builtin::kUndefined},
    {"jatgRx", Builtin::kUndefined},
    {"mb2x3", Builtin::kUndefined},
    {"mat2j4", Builtin::kUndefined},
    {"mt2x4", Builtin::kUndefined},
    {"m2q4", Builtin::kUndefined},
    {"matNN4f", Builtin::kUndefined},
    {"at24vv", Builtin::kUndefined},
    {"QQt2x4f", Builtin::kUndefined},
    {"maffxr", Builtin::kUndefined},
    {"mat2xjh", Builtin::kUndefined},
    {"mNNw2x48", Builtin::kUndefined},
    {"mt3x2", Builtin::kUndefined},
    {"rrat3x2", Builtin::kUndefined},
    {"mGt3x2", Builtin::kUndefined},
    {"mat3x2FF", Builtin::kUndefined},
    {"at3f", Builtin::kUndefined},
    {"marrx2f", Builtin::kUndefined},
    {"t3x2h", Builtin::kUndefined},
    {"Da3xJJh", Builtin::kUndefined},
    {"ma82", Builtin::kUndefined},
    {"1k33", Builtin::kUndefined},
    {"matx3", Builtin::kUndefined},
    {"maJx3", Builtin::kUndefined},
    {"mat3c3f", Builtin::kUndefined},
    {"mat3x3O", Builtin::kUndefined},
    {"KK_atvvtt3f", Builtin::kUndefined},
    {"xx83x3h", Builtin::kUndefined},
    {"__qatF3", Builtin::kUndefined},
    {"matqx3h", Builtin::kUndefined},
    {"ma33x66", Builtin::kUndefined},
    {"mttQQo3x4", Builtin::kUndefined},
    {"mat66x", Builtin::kUndefined},
    {"mtOxzz66", Builtin::kUndefined},
    {"mat3yy4f", Builtin::kUndefined},
    {"ZaHH4Z", Builtin::kUndefined},
    {"4WWt3q4h", Builtin::kUndefined},
    {"mOO3x4h", Builtin::kUndefined},
    {"oatY4h", Builtin::kUndefined},
    {"ax2", Builtin::kUndefined},
    {"ma4x2", Builtin::kUndefined},
    {"matw2", Builtin::kUndefined},
    {"fGtxKf", Builtin::kUndefined},
    {"matqKx2f", Builtin::kUndefined},
    {"matmmxFf", Builtin::kUndefined},
    {"at4x2h", Builtin::kUndefined},
    {"mt4x2q", Builtin::kUndefined},
    {"mat4xbb", Builtin::kUndefined},
    {"it4x3", Builtin::kUndefined},
    {"mOO4xq", Builtin::kUndefined},
    {"mat4Tvv3", Builtin::kUndefined},
    {"maFF4x3f", Builtin::kUndefined},
    {"Pa00xQf", Builtin::kUndefined},
    {"mPt4x3f", Builtin::kUndefined},
    {"ma774xss", Builtin::kUndefined},
    {"RRCbb4x3h", Builtin::kUndefined},
    {"mXXt4x3h", Builtin::kUndefined},
    {"CCt4OOOO", Builtin::kUndefined},
    {"mtsuL", Builtin::kUndefined},
    {"mat4xX", Builtin::kUndefined},
    {"mat44f", Builtin::kUndefined},
    {"qa4O4", Builtin::kUndefined},
    {"mat4x22f", Builtin::kUndefined},
    {"myzz40XX", Builtin::kUndefined},
    {"matVViP", Builtin::kUndefined},
    {"mannC4h", Builtin::kUndefined},
    {"pHAq", Builtin::kUndefined},
    {"tr", Builtin::kUndefined},
    {"Kf", Builtin::kUndefined},
    {"lmgger", Builtin::kUndefined},
    {"samplr", Builtin::kUndefined},
    {"NTTmcl4r", Builtin::kUndefined},
    {"sampler_clmppri77on", Builtin::kUndefined},
    {"samplg_czzmparNNso", Builtin::kUndefined},
    {"smpleuuXXomparibbon", Builtin::kUndefined},
    {"texture_1", Builtin::kUndefined},
    {"t88tueQ1K", Builtin::kUndefined},
    {"texturq9d", Builtin::kUndefined},
    {"text11re_2d", Builtin::kUndefined},
    {"teiiu22eF2d", Builtin::kUndefined},
    {"tex77ur_2d", Builtin::kUndefined},
    {"textNNr2_d_array", Builtin::kUndefined},
    {"textVVre_2d_array", Builtin::kUndefined},
    {"texwure_WWF_11rray", Builtin::kUndefined},
    {"txture_3ww", Builtin::kUndefined},
    {"texturD_3d", Builtin::kUndefined},
    {"teKture_d", Builtin::kUndefined},
    {"11exPPufe_cubh", Builtin::kUndefined},
    {"textue_cube", Builtin::kUndefined},
    {"texture_cubYY", Builtin::kUndefined},
    {"texttr_cube_HHkkVay", Builtin::kUndefined},
    {"texture_crrbe_array", Builtin::kUndefined},
    {"texturesscubeWWaray", Builtin::kUndefined},
    {"texture_deptY_d", Builtin::kUndefined},
    {"teLturq_defh_2d", Builtin::kUndefined},
    {"texvvre_duu22th_2d", Builtin::kUndefined},
    {"texure_deth_2d_array", Builtin::kUndefined},
    {"texturYY_depth_2daray", Builtin::kUndefined},
    {"texturE_77epth_2d_aryYay", Builtin::kUndefined},
    {"Mexdoore_depth_cue", Builtin::kUndefined},
    {"texturedepMMh_cube", Builtin::kUndefined},
    {"texture55depth_cube", Builtin::kUndefined},
    {"textue_depth_cbe_aNray", Builtin::kUndefined},
    {"texture_dpth_c33be_array", Builtin::kUndefined},
    {"texture_depth_cub3_array", Builtin::kUndefined},
    {"texIure_mepth_mulisampled_2d", Builtin::kUndefined},
    {"texture_depthrmKltisampled_2nn", Builtin::kUndefined},
    {"textur_depth_multismXld_2d", Builtin::kUndefined},
    {"texpure_exLLeIna", Builtin::kUndefined},
    {"txture_exfrnal", Builtin::kUndefined},
    {"teUture_extYRRDl", Builtin::kUndefined},
    {"texturehmultisampled_2d", Builtin::kUndefined},
    {"texturqmultsIImuuled_2d", Builtin::kUndefined},
    {"Hexture_multisampled_2d", Builtin::kUndefined},
    {"texQQur_storge_vvd", Builtin::kUndefined},
    {"texeure_66oage_1d", Builtin::kUndefined},
    {"texture_stoage71d", Builtin::kUndefined},
    {"texture_s55or0ge_2DD", Builtin::kUndefined},
    {"teHture_storIIge_2d", Builtin::kUndefined},
    {"textue_storage_2d", Builtin::kUndefined},
    {"texturestorage_2d_rrray", Builtin::kUndefined},
    {"textule_storage_2d_array", Builtin::kUndefined},
    {"tetture_JJtorage_Gd_arra", Builtin::kUndefined},
    {"yexture_storage3d", Builtin::kUndefined},
    {"texturestorage_3d", Builtin::kUndefined},
    {"texture_IItorBBge_3d", Builtin::kUndefined},
    {"TTK33", Builtin::kUndefined},
    {"nnUYdSS2", Builtin::kUndefined},
    {"x5dZ", Builtin::kUndefined},
    {"veckq", Builtin::kUndefined},
    {"ii500", Builtin::kUndefined},
    {"vecIIn", Builtin::kUndefined},
    {"cceW", Builtin::kUndefined},
    {"cKK", Builtin::kUndefined},
    {"vec66f", Builtin::kUndefined},
    {"vePPK", Builtin::kUndefined},
    {"vexxh", Builtin::kUndefined},
    {"qec2h", Builtin::kUndefined},
    {"veSyMMr", Builtin::kUndefined},
    {"v2u", Builtin::kUndefined},
    {"ec", Builtin::kUndefined},
    {"5eFF2u", Builtin::kUndefined},
    {"rrecz44", Builtin::kUndefined},
    {"vWW", Builtin::kUndefined},
    {"ZJJCcX", Builtin::kUndefined},
    {"vcPP", Builtin::kUndefined},
    {"vec", Builtin::kUndefined},
    {"3Le003f", Builtin::kUndefined},
    {"MMec3RR", Builtin::kUndefined},
    {"vec39K", Builtin::kUndefined},
    {"yyecm", Builtin::kUndefined},
    {"v__cD", Builtin::kUndefined},
    {"vec3U", Builtin::kUndefined},
    {"ze333i", Builtin::kUndefined},
    {"eKti", Builtin::kUndefined},
    {"ve3V", Builtin::kUndefined},
    {"jbR3K", Builtin::kUndefined},
    {"e44344", Builtin::kUndefined},
    {"00u", Builtin::kUndefined},
    {"WK4", Builtin::kUndefined},
    {"m", Builtin::kUndefined},
    {"vJJ", Builtin::kUndefined},
    {"lDDcUfC", Builtin::kUndefined},
    {"vec4g", Builtin::kUndefined},
    {"CCe", Builtin::kUndefined},
    {"ec4h", Builtin::kUndefined},
    {"vIc__h", Builtin::kUndefined},
    {"ePPtt", Builtin::kUndefined},
    {"v3dc4i", Builtin::kUndefined},
    {"vcyyi", Builtin::kUndefined},
    {"u4", Builtin::kUndefined},
    {"v03nnu", Builtin::kUndefined},
    {"Cuuecnv", Builtin::kUndefined},
    {"vX4ll", Builtin::kUndefined},
};

using BuiltinParseTest = testing::TestWithParam<Case>;

TEST_P(BuiltinParseTest, Parse) {
    const char* string = GetParam().string;
    Builtin expect = GetParam().value;
    EXPECT_EQ(expect, ParseBuiltin(string));
}

INSTANTIATE_TEST_SUITE_P(ValidCases, BuiltinParseTest, testing::ValuesIn(kValidCases));
INSTANTIATE_TEST_SUITE_P(InvalidCases, BuiltinParseTest, testing::ValuesIn(kInvalidCases));

using BuiltinPrintTest = testing::TestWithParam<Case>;

TEST_P(BuiltinPrintTest, Print) {
    Builtin value = GetParam().value;
    const char* expect = GetParam().string;
    EXPECT_EQ(expect, utils::ToString(value));
}

INSTANTIATE_TEST_SUITE_P(ValidCases, BuiltinPrintTest, testing::ValuesIn(kValidCases));

}  // namespace parse_print_tests

}  // namespace
}  // namespace tint::builtin

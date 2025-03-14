/*** Autogenerated by WIDL 6.3 from include/xaudio2fx.idl - Do not edit ***/

#ifdef _WIN32
#ifndef __REQUIRED_RPCNDR_H_VERSION__
#define __REQUIRED_RPCNDR_H_VERSION__ 475
#endif
#include <rpc.h>
#include <rpcndr.h>
#endif

#ifndef COM_NO_WINDOWS_H
#include <windows.h>
#include <ole2.h>
#endif

#ifndef __xaudio2fx_h__
#define __xaudio2fx_h__

/* Forward declarations */

#ifndef __AudioVolumeMeter20_FWD_DEFINED__
#define __AudioVolumeMeter20_FWD_DEFINED__
#ifdef __cplusplus
typedef class AudioVolumeMeter20 AudioVolumeMeter20;
#else
typedef struct AudioVolumeMeter20 AudioVolumeMeter20;
#endif /* defined __cplusplus */
#endif /* defined __AudioVolumeMeter20_FWD_DEFINED__ */

#ifndef __AudioVolumeMeter21_FWD_DEFINED__
#define __AudioVolumeMeter21_FWD_DEFINED__
#ifdef __cplusplus
typedef class AudioVolumeMeter21 AudioVolumeMeter21;
#else
typedef struct AudioVolumeMeter21 AudioVolumeMeter21;
#endif /* defined __cplusplus */
#endif /* defined __AudioVolumeMeter21_FWD_DEFINED__ */

#ifndef __AudioVolumeMeter22_FWD_DEFINED__
#define __AudioVolumeMeter22_FWD_DEFINED__
#ifdef __cplusplus
typedef class AudioVolumeMeter22 AudioVolumeMeter22;
#else
typedef struct AudioVolumeMeter22 AudioVolumeMeter22;
#endif /* defined __cplusplus */
#endif /* defined __AudioVolumeMeter22_FWD_DEFINED__ */

#ifndef __AudioVolumeMeter23_FWD_DEFINED__
#define __AudioVolumeMeter23_FWD_DEFINED__
#ifdef __cplusplus
typedef class AudioVolumeMeter23 AudioVolumeMeter23;
#else
typedef struct AudioVolumeMeter23 AudioVolumeMeter23;
#endif /* defined __cplusplus */
#endif /* defined __AudioVolumeMeter23_FWD_DEFINED__ */

#ifndef __AudioVolumeMeter24_FWD_DEFINED__
#define __AudioVolumeMeter24_FWD_DEFINED__
#ifdef __cplusplus
typedef class AudioVolumeMeter24 AudioVolumeMeter24;
#else
typedef struct AudioVolumeMeter24 AudioVolumeMeter24;
#endif /* defined __cplusplus */
#endif /* defined __AudioVolumeMeter24_FWD_DEFINED__ */

#ifndef __AudioVolumeMeter25_FWD_DEFINED__
#define __AudioVolumeMeter25_FWD_DEFINED__
#ifdef __cplusplus
typedef class AudioVolumeMeter25 AudioVolumeMeter25;
#else
typedef struct AudioVolumeMeter25 AudioVolumeMeter25;
#endif /* defined __cplusplus */
#endif /* defined __AudioVolumeMeter25_FWD_DEFINED__ */

#ifndef __AudioVolumeMeter26_FWD_DEFINED__
#define __AudioVolumeMeter26_FWD_DEFINED__
#ifdef __cplusplus
typedef class AudioVolumeMeter26 AudioVolumeMeter26;
#else
typedef struct AudioVolumeMeter26 AudioVolumeMeter26;
#endif /* defined __cplusplus */
#endif /* defined __AudioVolumeMeter26_FWD_DEFINED__ */

#ifndef __AudioVolumeMeter27_FWD_DEFINED__
#define __AudioVolumeMeter27_FWD_DEFINED__
#ifdef __cplusplus
typedef class AudioVolumeMeter27 AudioVolumeMeter27;
#else
typedef struct AudioVolumeMeter27 AudioVolumeMeter27;
#endif /* defined __cplusplus */
#endif /* defined __AudioVolumeMeter27_FWD_DEFINED__ */

#ifndef __AudioReverb20_FWD_DEFINED__
#define __AudioReverb20_FWD_DEFINED__
#ifdef __cplusplus
typedef class AudioReverb20 AudioReverb20;
#else
typedef struct AudioReverb20 AudioReverb20;
#endif /* defined __cplusplus */
#endif /* defined __AudioReverb20_FWD_DEFINED__ */

#ifndef __AudioReverb21_FWD_DEFINED__
#define __AudioReverb21_FWD_DEFINED__
#ifdef __cplusplus
typedef class AudioReverb21 AudioReverb21;
#else
typedef struct AudioReverb21 AudioReverb21;
#endif /* defined __cplusplus */
#endif /* defined __AudioReverb21_FWD_DEFINED__ */

#ifndef __AudioReverb22_FWD_DEFINED__
#define __AudioReverb22_FWD_DEFINED__
#ifdef __cplusplus
typedef class AudioReverb22 AudioReverb22;
#else
typedef struct AudioReverb22 AudioReverb22;
#endif /* defined __cplusplus */
#endif /* defined __AudioReverb22_FWD_DEFINED__ */

#ifndef __AudioReverb23_FWD_DEFINED__
#define __AudioReverb23_FWD_DEFINED__
#ifdef __cplusplus
typedef class AudioReverb23 AudioReverb23;
#else
typedef struct AudioReverb23 AudioReverb23;
#endif /* defined __cplusplus */
#endif /* defined __AudioReverb23_FWD_DEFINED__ */

#ifndef __AudioReverb24_FWD_DEFINED__
#define __AudioReverb24_FWD_DEFINED__
#ifdef __cplusplus
typedef class AudioReverb24 AudioReverb24;
#else
typedef struct AudioReverb24 AudioReverb24;
#endif /* defined __cplusplus */
#endif /* defined __AudioReverb24_FWD_DEFINED__ */

#ifndef __AudioReverb25_FWD_DEFINED__
#define __AudioReverb25_FWD_DEFINED__
#ifdef __cplusplus
typedef class AudioReverb25 AudioReverb25;
#else
typedef struct AudioReverb25 AudioReverb25;
#endif /* defined __cplusplus */
#endif /* defined __AudioReverb25_FWD_DEFINED__ */

#ifndef __AudioReverb26_FWD_DEFINED__
#define __AudioReverb26_FWD_DEFINED__
#ifdef __cplusplus
typedef class AudioReverb26 AudioReverb26;
#else
typedef struct AudioReverb26 AudioReverb26;
#endif /* defined __cplusplus */
#endif /* defined __AudioReverb26_FWD_DEFINED__ */

#ifndef __AudioReverb27_FWD_DEFINED__
#define __AudioReverb27_FWD_DEFINED__
#ifdef __cplusplus
typedef class AudioReverb27 AudioReverb27;
#else
typedef struct AudioReverb27 AudioReverb27;
#endif /* defined __cplusplus */
#endif /* defined __AudioReverb27_FWD_DEFINED__ */

/* Headers for imported files */

#include <unknwn.h>

#ifdef __cplusplus
extern "C" {
#endif

/*****************************************************************************
 * AudioVolumeMeter20 coclass
 */

DEFINE_GUID(CLSID_AudioVolumeMeter20, 0xc0c56f46, 0x29b1, 0x44e9, 0x99,0x39, 0xa3,0x2c,0xe8,0x68,0x67,0xe2);

#ifdef __cplusplus
class DECLSPEC_UUID("c0c56f46-29b1-44e9-9939-a32ce86867e2") AudioVolumeMeter20;
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(AudioVolumeMeter20, 0xc0c56f46, 0x29b1, 0x44e9, 0x99,0x39, 0xa3,0x2c,0xe8,0x68,0x67,0xe2)
#endif
#endif

/*****************************************************************************
 * AudioVolumeMeter21 coclass
 */

DEFINE_GUID(CLSID_AudioVolumeMeter21, 0xc1e3f122, 0xa2ea, 0x442c, 0x85,0x4f, 0x20,0xd9,0x8f,0x83,0x57,0xa1);

#ifdef __cplusplus
class DECLSPEC_UUID("c1e3f122-a2ea-442c-854f-20d98f8357a1") AudioVolumeMeter21;
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(AudioVolumeMeter21, 0xc1e3f122, 0xa2ea, 0x442c, 0x85,0x4f, 0x20,0xd9,0x8f,0x83,0x57,0xa1)
#endif
#endif

/*****************************************************************************
 * AudioVolumeMeter22 coclass
 */

DEFINE_GUID(CLSID_AudioVolumeMeter22, 0xf5ca7b34, 0x8055, 0x42c0, 0xb8,0x36, 0x21,0x61,0x29,0xeb,0x7e,0x30);

#ifdef __cplusplus
class DECLSPEC_UUID("f5ca7b34-8055-42c0-b836-216129eb7e30") AudioVolumeMeter22;
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(AudioVolumeMeter22, 0xf5ca7b34, 0x8055, 0x42c0, 0xb8,0x36, 0x21,0x61,0x29,0xeb,0x7e,0x30)
#endif
#endif

/*****************************************************************************
 * AudioVolumeMeter23 coclass
 */

DEFINE_GUID(CLSID_AudioVolumeMeter23, 0xe180344b, 0xac83, 0x4483, 0x95,0x9e, 0x18,0xa5,0xc5,0x6a,0x5e,0x19);

#ifdef __cplusplus
class DECLSPEC_UUID("e180344b-ac83-4483-959e-18a5c56a5e19") AudioVolumeMeter23;
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(AudioVolumeMeter23, 0xe180344b, 0xac83, 0x4483, 0x95,0x9e, 0x18,0xa5,0xc5,0x6a,0x5e,0x19)
#endif
#endif

/*****************************************************************************
 * AudioVolumeMeter24 coclass
 */

DEFINE_GUID(CLSID_AudioVolumeMeter24, 0xc7338b95, 0x52b8, 0x4542, 0xaa,0x79, 0x42,0xeb,0x01,0x6c,0x8c,0x1c);

#ifdef __cplusplus
class DECLSPEC_UUID("c7338b95-52b8-4542-aa79-42eb016c8c1c") AudioVolumeMeter24;
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(AudioVolumeMeter24, 0xc7338b95, 0x52b8, 0x4542, 0xaa,0x79, 0x42,0xeb,0x01,0x6c,0x8c,0x1c)
#endif
#endif

/*****************************************************************************
 * AudioVolumeMeter25 coclass
 */

DEFINE_GUID(CLSID_AudioVolumeMeter25, 0x2139e6da, 0xc341, 0x4774, 0x9a,0xc3, 0xb4,0xe0,0x26,0x34,0x7f,0x64);

#ifdef __cplusplus
class DECLSPEC_UUID("2139e6da-c341-4774-9ac3-b4e026347f64") AudioVolumeMeter25;
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(AudioVolumeMeter25, 0x2139e6da, 0xc341, 0x4774, 0x9a,0xc3, 0xb4,0xe0,0x26,0x34,0x7f,0x64)
#endif
#endif

/*****************************************************************************
 * AudioVolumeMeter26 coclass
 */

DEFINE_GUID(CLSID_AudioVolumeMeter26, 0xe48c5a3f, 0x93ef, 0x43bb, 0xa0,0x92, 0x2c,0x7c,0xeb,0x94,0x6f,0x27);

#ifdef __cplusplus
class DECLSPEC_UUID("e48c5a3f-93ef-43bb-a092-2c7ceb946f27") AudioVolumeMeter26;
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(AudioVolumeMeter26, 0xe48c5a3f, 0x93ef, 0x43bb, 0xa0,0x92, 0x2c,0x7c,0xeb,0x94,0x6f,0x27)
#endif
#endif

/*****************************************************************************
 * AudioVolumeMeter27 coclass
 */

DEFINE_GUID(CLSID_AudioVolumeMeter27, 0xcac1105f, 0x619b, 0x4d04, 0x83,0x1a, 0x44,0xe1,0xcb,0xf1,0x2d,0x57);

#ifdef __cplusplus
class DECLSPEC_UUID("cac1105f-619b-4d04-831a-44e1cbf12d57") AudioVolumeMeter27;
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(AudioVolumeMeter27, 0xcac1105f, 0x619b, 0x4d04, 0x83,0x1a, 0x44,0xe1,0xcb,0xf1,0x2d,0x57)
#endif
#endif

/*****************************************************************************
 * AudioReverb20 coclass
 */

DEFINE_GUID(CLSID_AudioReverb20, 0x6f6ea3a9, 0x2cf5, 0x41cf, 0x91,0xc1, 0x21,0x70,0xb1,0x54,0x00,0x63);

#ifdef __cplusplus
class DECLSPEC_UUID("6f6ea3a9-2cf5-41cf-91c1-2170b1540063") AudioReverb20;
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(AudioReverb20, 0x6f6ea3a9, 0x2cf5, 0x41cf, 0x91,0xc1, 0x21,0x70,0xb1,0x54,0x00,0x63)
#endif
#endif

/*****************************************************************************
 * AudioReverb21 coclass
 */

DEFINE_GUID(CLSID_AudioReverb21, 0xf4769300, 0xb949, 0x4df9, 0xb3,0x33, 0x00,0xd3,0x39,0x32,0xe9,0xa6);

#ifdef __cplusplus
class DECLSPEC_UUID("f4769300-b949-4df9-b333-00d33932e9a6") AudioReverb21;
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(AudioReverb21, 0xf4769300, 0xb949, 0x4df9, 0xb3,0x33, 0x00,0xd3,0x39,0x32,0xe9,0xa6)
#endif
#endif

/*****************************************************************************
 * AudioReverb22 coclass
 */

DEFINE_GUID(CLSID_AudioReverb22, 0x629cf0de, 0x3ecc, 0x41e7, 0x99,0x26, 0xf7,0xe4,0x3e,0xeb,0xec,0x51);

#ifdef __cplusplus
class DECLSPEC_UUID("629cf0de-3ecc-41e7-9926-f7e43eebec51") AudioReverb22;
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(AudioReverb22, 0x629cf0de, 0x3ecc, 0x41e7, 0x99,0x26, 0xf7,0xe4,0x3e,0xeb,0xec,0x51)
#endif
#endif

/*****************************************************************************
 * AudioReverb23 coclass
 */

DEFINE_GUID(CLSID_AudioReverb23, 0x9cab402c, 0x1d37, 0x44b4, 0x88,0x6d, 0xfa,0x4f,0x36,0x17,0x0a,0x4c);

#ifdef __cplusplus
class DECLSPEC_UUID("9cab402c-1d37-44b4-886d-fa4f36170a4c") AudioReverb23;
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(AudioReverb23, 0x9cab402c, 0x1d37, 0x44b4, 0x88,0x6d, 0xfa,0x4f,0x36,0x17,0x0a,0x4c)
#endif
#endif

/*****************************************************************************
 * AudioReverb24 coclass
 */

DEFINE_GUID(CLSID_AudioReverb24, 0x8bb7778b, 0x645b, 0x4475, 0x9a,0x73, 0x1d,0xe3,0x17,0x0b,0xd3,0xaf);

#ifdef __cplusplus
class DECLSPEC_UUID("8bb7778b-645b-4475-9a73-1de3170bd3af") AudioReverb24;
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(AudioReverb24, 0x8bb7778b, 0x645b, 0x4475, 0x9a,0x73, 0x1d,0xe3,0x17,0x0b,0xd3,0xaf)
#endif
#endif

/*****************************************************************************
 * AudioReverb25 coclass
 */

DEFINE_GUID(CLSID_AudioReverb25, 0xd06df0d0, 0x8518, 0x441e, 0x82,0x2f, 0x54,0x51,0xd5,0xc5,0x95,0xb8);

#ifdef __cplusplus
class DECLSPEC_UUID("d06df0d0-8518-441e-822f-5451d5c595b8") AudioReverb25;
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(AudioReverb25, 0xd06df0d0, 0x8518, 0x441e, 0x82,0x2f, 0x54,0x51,0xd5,0xc5,0x95,0xb8)
#endif
#endif

/*****************************************************************************
 * AudioReverb26 coclass
 */

DEFINE_GUID(CLSID_AudioReverb26, 0xcecec95a, 0xd894, 0x491a, 0xbe,0xe3, 0x5e,0x10,0x6f,0xb5,0x9f,0x2d);

#ifdef __cplusplus
class DECLSPEC_UUID("cecec95a-d894-491a-bee3-5e106fb59f2d") AudioReverb26;
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(AudioReverb26, 0xcecec95a, 0xd894, 0x491a, 0xbe,0xe3, 0x5e,0x10,0x6f,0xb5,0x9f,0x2d)
#endif
#endif

/*****************************************************************************
 * AudioReverb27 coclass
 */

DEFINE_GUID(CLSID_AudioReverb27, 0x6a93130e, 0x1d53, 0x41d1, 0xa9,0xcf, 0xe7,0x58,0x80,0x0b,0xb1,0x79);

#ifdef __cplusplus
class DECLSPEC_UUID("6a93130e-1d53-41d1-a9cf-e758800bb179") AudioReverb27;
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(AudioReverb27, 0x6a93130e, 0x1d53, 0x41d1, 0xa9,0xcf, 0xe7,0x58,0x80,0x0b,0xb1,0x79)
#endif
#endif

/* Begin additional prototypes for all interfaces */


/* End additional prototypes */

#ifdef __cplusplus
}
#endif

#endif /* __xaudio2fx_h__ */

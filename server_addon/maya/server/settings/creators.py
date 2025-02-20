from pydantic import Field

from ayon_server.settings import BaseSettingsModel


class CreateLookModel(BaseSettingsModel):
    enabled: bool = Field(title="Enabled")
    make_tx: bool = Field(title="Make tx files")
    rs_tex: bool = Field(title="Make Redshift texture files")
    default_variants: list[str] = Field(
        default_factory=list, title="Default Products"
    )


class BasicCreatorModel(BaseSettingsModel):
    enabled: bool = Field(title="Enabled")
    default_variants: list[str] = Field(
        default_factory=list,
        title="Default Products"
    )


class CreateUnrealStaticMeshModel(BaseSettingsModel):
    enabled: bool = Field(title="Enabled")
    default_variants: list[str] = Field(
        default_factory=list,
        title="Default Products"
    )
    static_mesh_prefixes: str = Field("S", title="Static Mesh Prefix")
    collision_prefixes: list[str] = Field(
        default_factory=list,
        title="Collision Prefixes"
    )


class CreateUnrealSkeletalMeshModel(BaseSettingsModel):
    enabled: bool = Field(title="Enabled")
    default_variants: list[str] = Field(
        default_factory=list, title="Default Products")
    joint_hints: str = Field("jnt_org", title="Joint root hint")


class CreateMultiverseLookModel(BaseSettingsModel):
    enabled: bool = Field(title="Enabled")
    publish_mip_map: bool = Field(title="publish_mip_map")


class BasicExportMeshModel(BaseSettingsModel):
    enabled: bool = Field(title="Enabled")
    write_color_sets: bool = Field(title="Write Color Sets")
    write_face_sets: bool = Field(title="Write Face Sets")
    default_variants: list[str] = Field(
        default_factory=list,
        title="Default Products"
    )


class CreateAnimationModel(BaseSettingsModel):
    write_color_sets: bool = Field(title="Write Color Sets")
    write_face_sets: bool = Field(title="Write Face Sets")
    include_parent_hierarchy: bool = Field(
        title="Include Parent Hierarchy")
    include_user_defined_attributes: bool = Field(
        title="Include User Defined Attributes")
    default_variants: list[str] = Field(
        default_factory=list,
        title="Default Products"
    )


class CreatePointCacheModel(BaseSettingsModel):
    enabled: bool = Field(title="Enabled")
    write_color_sets: bool = Field(title="Write Color Sets")
    write_face_sets: bool = Field(title="Write Face Sets")
    include_user_defined_attributes: bool = Field(
        title="Include User Defined Attributes"
    )
    default_variants: list[str] = Field(
        default_factory=list,
        title="Default Products"
    )


class CreateProxyAlembicModel(BaseSettingsModel):
    enabled: bool = Field(title="Enabled")
    write_color_sets: bool = Field(title="Write Color Sets")
    write_face_sets: bool = Field(title="Write Face Sets")
    default_variants: list[str] = Field(
        default_factory=list,
        title="Default Products"
    )


class CreateAssModel(BasicCreatorModel):
    expandProcedurals: bool = Field(title="Expand Procedurals")
    motionBlur: bool = Field(title="Motion Blur")
    motionBlurKeys: int = Field(2, title="Motion Blur Keys")
    motionBlurLength: float = Field(0.5, title="Motion Blur Length")
    maskOptions: bool = Field(title="Mask Options")
    maskCamera: bool = Field(title="Mask Camera")
    maskLight: bool = Field(title="Mask Light")
    maskShape: bool = Field(title="Mask Shape")
    maskShader: bool = Field(title="Mask Shader")
    maskOverride: bool = Field(title="Mask Override")
    maskDriver: bool = Field(title="Mask Driver")
    maskFilter: bool = Field(title="Mask Filter")
    maskColor_manager: bool = Field(title="Mask Color Manager")
    maskOperator: bool = Field(title="Mask Operator")


class CreateReviewModel(BasicCreatorModel):
    useMayaTimeline: bool = Field(title="Use Maya Timeline for Frame Range.")


class CreateVrayProxyModel(BaseSettingsModel):
    enabled: bool = Field(True)
    vrmesh: bool = Field(title="VrMesh")
    alembic: bool = Field(title="Alembic")
    default_variants: list[str] = Field(
        default_factory=list, title="Default Products")


class CreatorsModel(BaseSettingsModel):
    CreateLook: CreateLookModel = Field(
        default_factory=CreateLookModel,
        title="Create Look"
    )
    CreateRender: BasicCreatorModel = Field(
        default_factory=BasicCreatorModel,
        title="Create Render"
    )
    # "-" is not compatible in the new model
    CreateUnrealStaticMesh: CreateUnrealStaticMeshModel = Field(
        default_factory=CreateUnrealStaticMeshModel,
        title="Create Unreal_Static Mesh"
    )
    # "-" is not compatible in the new model
    CreateUnrealSkeletalMesh: CreateUnrealSkeletalMeshModel = Field(
        default_factory=CreateUnrealSkeletalMeshModel,
        title="Create Unreal_Skeletal Mesh"
    )
    CreateMultiverseLook: CreateMultiverseLookModel = Field(
        default_factory=CreateMultiverseLookModel,
        title="Create Multiverse Look"
    )
    CreateAnimation: CreateAnimationModel = Field(
        default_factory=CreateAnimationModel,
        title="Create Animation"
    )
    CreateModel: BasicExportMeshModel = Field(
        default_factory=BasicExportMeshModel,
        title="Create Model"
    )
    CreatePointCache: CreatePointCacheModel = Field(
        default_factory=CreatePointCacheModel,
        title="Create Point Cache"
    )
    CreateProxyAlembic: CreateProxyAlembicModel = Field(
        default_factory=CreateProxyAlembicModel,
        title="Create Proxy Alembic"
    )
    CreateMultiverseUsd: BasicCreatorModel = Field(
        default_factory=BasicCreatorModel,
        title="Create Multiverse USD"
    )
    CreateMultiverseUsdComp: BasicCreatorModel = Field(
        default_factory=BasicCreatorModel,
        title="Create Multiverse USD Composition"
    )
    CreateMultiverseUsdOver: BasicCreatorModel = Field(
        default_factory=BasicCreatorModel,
        title="Create Multiverse USD Override"
    )
    CreateAss: CreateAssModel = Field(
        default_factory=CreateAssModel,
        title="Create Ass"
    )
    CreateAssembly: BasicCreatorModel = Field(
        default_factory=BasicCreatorModel,
        title="Create Assembly"
    )
    CreateCamera: BasicCreatorModel = Field(
        default_factory=BasicCreatorModel,
        title="Create Camera"
    )
    CreateLayout: BasicCreatorModel = Field(
        default_factory=BasicCreatorModel,
        title="Create Layout"
    )
    CreateMayaScene: BasicCreatorModel = Field(
        default_factory=BasicCreatorModel,
        title="Create Maya Scene"
    )
    CreateRenderSetup: BasicCreatorModel = Field(
        default_factory=BasicCreatorModel,
        title="Create Render Setup"
    )
    CreateReview: CreateReviewModel = Field(
        default_factory=CreateReviewModel,
        title="Create Review"
    )
    CreateRig: BasicCreatorModel = Field(
        default_factory=BasicCreatorModel,
        title="Create Rig"
    )
    CreateSetDress: BasicCreatorModel = Field(
        default_factory=BasicCreatorModel,
        title="Create Set Dress"
    )
    CreateVrayProxy: CreateVrayProxyModel = Field(
        default_factory=CreateVrayProxyModel,
        title="Create VRay Proxy"
    )
    CreateVRayScene: BasicCreatorModel = Field(
        default_factory=BasicCreatorModel,
        title="Create VRay Scene"
    )
    CreateYetiRig: BasicCreatorModel = Field(
        default_factory=BasicCreatorModel,
        title="Create Yeti Rig"
    )


DEFAULT_CREATORS_SETTINGS = {
    "CreateLook": {
        "enabled": True,
        "make_tx": True,
        "rs_tex": False,
        "default_variants": [
            "Main"
        ]
    },
    "CreateRender": {
        "enabled": True,
        "default_variants": [
            "Main"
        ]
    },
    "CreateUnrealStaticMesh": {
        "enabled": True,
        "default_variants": [
            "",
            "_Main"
        ],
        "static_mesh_prefix": "S",
        "collision_prefixes": [
            "UBX",
            "UCP",
            "USP",
            "UCX"
        ]
    },
    "CreateUnrealSkeletalMesh": {
        "enabled": True,
        "default_variants": [],
        "joint_hints": "jnt_org"
    },
    "CreateMultiverseLook": {
        "enabled": True,
        "publish_mip_map": True
    },
    "CreateAnimation": {
        "write_color_sets": False,
        "write_face_sets": False,
        "include_parent_hierarchy": False,
        "include_user_defined_attributes": False,
        "default_variants": [
            "Main"
        ]
    },
    "CreateModel": {
        "enabled": True,
        "write_color_sets": False,
        "write_face_sets": False,
        "default_variants": [
            "Main",
            "Proxy",
            "Sculpt"
        ]
    },
    "CreatePointCache": {
        "enabled": True,
        "write_color_sets": False,
        "write_face_sets": False,
        "include_user_defined_attributes": False,
        "default_variants": [
            "Main"
        ]
    },
    "CreateProxyAlembic": {
        "enabled": True,
        "write_color_sets": False,
        "write_face_sets": False,
        "default_variants": [
            "Main"
        ]
    },
    "CreateMultiverseUsd": {
        "enabled": True,
        "default_variants": [
            "Main"
        ]
    },
    "CreateMultiverseUsdComp": {
        "enabled": True,
        "default_variants": [
            "Main"
        ]
    },
    "CreateMultiverseUsdOver": {
        "enabled": True,
        "default_variants": [
            "Main"
        ]
    },
    "CreateAss": {
        "enabled": True,
        "default_variants": [
            "Main"
        ],
        "expandProcedurals": False,
        "motionBlur": True,
        "motionBlurKeys": 2,
        "motionBlurLength": 0.5,
        "maskOptions": False,
        "maskCamera": False,
        "maskLight": False,
        "maskShape": False,
        "maskShader": False,
        "maskOverride": False,
        "maskDriver": False,
        "maskFilter": False,
        "maskColor_manager": False,
        "maskOperator": False
    },
    "CreateAssembly": {
        "enabled": True,
        "default_variants": [
            "Main"
        ]
    },
    "CreateCamera": {
        "enabled": True,
        "default_variants": [
            "Main"
        ]
    },
    "CreateLayout": {
        "enabled": True,
        "default_variants": [
            "Main"
        ]
    },
    "CreateMayaScene": {
        "enabled": True,
        "default_variants": [
            "Main"
        ]
    },
    "CreateRenderSetup": {
        "enabled": True,
        "default_variants": [
            "Main"
        ]
    },
    "CreateReview": {
        "enabled": True,
        "default_variants": [
            "Main"
        ],
        "useMayaTimeline": True
    },
    "CreateRig": {
        "enabled": True,
        "default_variants": [
            "Main",
            "Sim",
            "Cloth"
        ]
    },
    "CreateSetDress": {
        "enabled": True,
        "default_variants": [
            "Main",
            "Anim"
        ]
    },
    "CreateVrayProxy": {
        "enabled": True,
        "vrmesh": True,
        "alembic": True,
        "default_variants": [
            "Main"
        ]
    },
    "CreateVRayScene": {
        "enabled": True,
        "default_variants": [
            "Main"
        ]
    },
    "CreateYetiRig": {
        "enabled": True,
        "default_variants": [
            "Main"
        ]
    }
}

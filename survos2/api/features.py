import hug
import os.path as op

from survos2.api import workspace as ws
from survos2.api.utils import get_function_api, save_metadata, dataset_repr
from survos2.api.types import DataURI, String, Int, Float, FloatOrVector, SmartBoolean

from survos2.io import dataset_from_uri
from survos2.utils import get_logger
from survos2.improc import map_blocks


__feature_group__ = "features"
__feature_dtype__ = "float32"
__feature_fill__ = 0


# logger = get_logger()
from loguru import logger


def pass_through(x):
    return x


@hug.get()
@save_metadata
def structure_tensor_determinant(
    src: DataURI, dst: DataURI, sigma: FloatOrVector = 1
) -> "BLOB":
    """
    API wrapper around `survos2.improc.features.blob.compute_structure_tensor_determinant`.
    """
    from ..server.filtering.blob import compute_structure_tensor_determinant

    map_blocks(
        compute_structure_tensor_determinant, src, out=dst, sigma=sigma, normalize=True
    )


@hug.get()
@save_metadata
def hessian(src: DataURI, dst: DataURI, sigma: FloatOrVector = 1) -> "BLOB":
    from ..server.filtering.blob import compute_hessian_determinant

    map_blocks(compute_hessian_determinant, src, out=dst, sigma=sigma, normalize=True)


@hug.get()
@save_metadata
def frangi(
    src: DataURI,
    dst: DataURI,
    scale_min: Float = 1.0,
    scale_max: Float = 4.0,
    scale_step: Float = 1.0,
    alpha: Float = 0.5,
    beta: Float = 0.5,
    gamma=15,
) -> "BLOB":
    from ..server.filtering.blob import compute_frangi

    map_blocks(
        compute_frangi,
        src,
        out=dst,
        scale_range=(scale_min, scale_max),
        scale_step=1.0,
        alpha=0.5,
        beta=0.5,
        gamma=15,
        dark_response=True,
        normalize=True,
    )


@hug.get()
@save_metadata
def hessian_eigvals(src: DataURI, dst: DataURI, sigma: FloatOrVector = 1) -> "BLOB":
    from ..server.filtering.blob import hessian_eigvals_image

    map_blocks(hessian_eigvals_image, src, out=dst, sigma=sigma, normalize=True)


@hug.get()
@save_metadata
def hessian_eigvals_cython(
    src: DataURI, dst: DataURI, sigma: FloatOrVector = 1
) -> "BLOB":
    from ..server.filtering.blob import hessian_eigvals_cython

    map_blocks(hessian_eigvals_cython, src, out=dst, sigma=sigma, normalize=True)


@hug.get()
@save_metadata
def raw(src: DataURI, dst: DataURI) -> "BASE":
    map_blocks(pass_through, src, out=dst, normalize=True)


@hug.get()
@save_metadata
def simple_invert(src: DataURI, dst: DataURI) -> "BASE":
    from ..server.filtering import simple_invert

    map_blocks(simple_invert, src, out=dst, normalize=True)


@hug.get()
@save_metadata
def gamma_correct(src: DataURI, dst: DataURI, gamma: Float = 1.0) -> "BASE":
    from ..server.filtering import gamma_adjust

    map_blocks(gamma_adjust, src, gamma=gamma, out=dst, normalize=True)


@hug.get()
@save_metadata
def dilation(src: DataURI, dst: DataURI, num_iter: Int = 1) -> "MORPHOLOGY":
    from ..server.filtering import dilate

    map_blocks(dilate, src, num_iter=num_iter, out=dst, normalize=True)


@hug.get()
@save_metadata
def erosion(src: DataURI, dst: DataURI, num_iter: Int = 1) -> "MORPHOLOGY":
    from ..server.filtering import erode

    map_blocks(erode, src, num_iter=num_iter, out=dst, normalize=True)


@hug.get()
@save_metadata
def total_variation(
    src: DataURI, dst: DataURI, lamda: Float = 10, max_iter: Int = 100
) -> "DENOISING":
    """
    API wrapper around `survos2.improc.features.tv.tvdenoising3d`.
    """
    from ..improc.features.tv import tvdenoising3d

    map_blocks(
        tvdenoising3d, src, out=dst, lamda=lamda, max_iter=max_iter, normalize=True
    )


@hug.get()
@save_metadata
def tvdenoise_kornia(
    src: DataURI,
    dst: DataURI,
    regularization_amount: Float = 0.001,
    pad: Int = 8,
    max_iter: Int = 100,
) -> "DENOISING":
    """
    API wrapper around `survos2.improc.features.tv.tvdenoising3d`.
    """
    from ..server.filtering.blur import tvdenoise_kornia

    map_blocks(
        tvdenoise_kornia,
        src,
        out=dst,
        regularization_amount=regularization_amount,
        max_iter=max_iter,
        pad=pad,
        normalize=True,
    )


@hug.get()
@save_metadata
def spatial_gradient_3d(src: DataURI, dst: DataURI, dim: Int = 0) -> "EDGES":
    from ..server.filtering import spatial_gradient_3d

    map_blocks(spatial_gradient_3d, src, out=dst, dim=dim, normalize=True)


@hug.get()
@save_metadata
def difference_of_gaussians(
    src: DataURI, dst: DataURI, sigma: FloatOrVector = 1, sigma_ratio: Float = 1
) -> "EDGES":
    from ..server.filtering.edge import compute_difference_gaussians

    map_blocks(
        compute_difference_gaussians,
        src,
        out=dst,
        sigma=sigma,
        sigma_ratio=sigma_ratio,
        normalize=True,
    )


@hug.get()
@save_metadata
def gaussian_blur(src: DataURI, dst: DataURI, sigma: FloatOrVector = 1 ) -> "DENOISING":
    from ..server.filtering import gaussian_blur_kornia

    if isinstance(sigma, numbers.Number):
        sigma = (sigma, sigma, sigma)
    map_blocks(
        gaussian_blur_kornia,
        src,
        out=dst,
        sigma=sigma,
        pad=max(4, int((max(sigma) + 1) / 2)),
        normalize=True,
    )


@hug.get()
@save_metadata
def gaussian(src: DataURI, dst: DataURI, sigma: FloatOrVector = 1) -> "DENOISING":
    """
    API wrapper around `survos2.improc.features.gauss.gaussian`.
    """
    from ..improc.features.gauss import gaussian

    map_blocks(gaussian, src, out=dst, sigma=sigma, normalize=True)


@hug.get()
@save_metadata
def ndimage_laplacian(
    src: DataURI, dst: DataURI, kernel_size: FloatOrVector = 1
) -> "EDGES":
    from ..server.filtering import ndimage_laplacian

    map_blocks(
        ndimage_laplacian,
        src,
        out=dst,
        kernel_size=kernel_size,
        pad=max(4, int((max(kernel_size) + 1) / 2)),
        normalize=True,
    )


@hug.get()
@save_metadata
def laplacian(src: DataURI, dst: DataURI, kernel_size: Float = 2.0) -> "EDGES":
    from ..server.filtering.edge import laplacian

    map_blocks(
        laplacian,
        src,
        out=dst,
        kernel_size=kernel_size,
        pad=max(4, int(kernel_size) + 1 / 2),
        normalize=True,
    )


@hug.get()
@save_metadata
def gaussian_norm(src: DataURI, dst: DataURI, sigma: FloatOrVector = 1) -> "DENOISING":
    """
    API wrapper around `survos2.improc.features.gauss.gaussian_norm`.
    """
    from ..server.filtering.blur import gaussian_norm

    map_blocks(
        gaussian_norm,
        src,
        out=dst,
        sigma=sigma,
        pad=max(4, int((max(sigma) + 1) / 2)),
        normalize=True,
    )


@hug.get()
@save_metadata
def gaussian_center(
    src: DataURI, dst: DataURI, sigma: FloatOrVector = 1
) -> "DENOISING":
    """
    API wrapper around `survos2.improc.features.gauss.gaussian_center`.
    """
    from ..server.filtering.blur import gaussian_center

    map_blocks(
        gaussian_center,
        src,
        out=dst,
        sigma=sigma,
        pad=max(4, int((max(kernel_size) + 1) / 2)),
        normalize=True,
    )


@hug.get()
@save_metadata
def median(
    src: DataURI, dst: DataURI, median_size: Int = 1, num_iter: Int = 1
) -> "DENOISING":
    from ..server.filtering import median

    map_blocks(
        median,
        src,
        median_size=median_size,
        num_iter=num_iter,
        out=dst,
        pad=0,
        normalize=False,
    )


@hug.get()
@save_metadata
def local_mean(src: DataURI, dst: DataURI, radius: FloatOrVector = 1) -> "LOCAL":
    """
    API wrapper around `survos2.improc.features.gauss.gaussian_norm`.
    """
    from ..improc.features.local import compute_local_mean

    map_blocks(
        compute_local_mean,
        src,
        out=dst,
        radius=radius,
        pad=max(4, int((max(radius) + 1) / 2)),
        normalize=True,
    )


@hug.get()
@save_metadata
def local_std(src: DataURI, dst: DataURI, radius: FloatOrVector = 1) -> "LOCAL":
    """
    API wrapper around `survos2.improc.features.gauss.gaussian_norm`.
    """
    from ..improc.features.local import compute_local_std

    map_blocks(
        compute_local_std,
        src,
        out=dst,
        radius=radius,
        pad=max(4, int((max(radius) + 1) / 2)),
        normalize=True,
    )


@hug.get()
def create(workspace: String, feature_type: String):
    ds = ws.auto_create_dataset(
        workspace,
        feature_type,
        __feature_group__,
        __feature_dtype__,
        fill=__feature_fill__,
    )
    ds.set_attr("kind", feature_type)
    logger.debug(f"Created (empty) feature of kind {feature_type}")
    return dataset_repr(ds)


@hug.get()
@hug.local()
def existing(
    workspace: String, full: SmartBoolean = False, filter: SmartBoolean = True
):
    datasets = ws.existing_datasets(workspace, group=__feature_group__)
    if full:
        datasets = {
            "{}/{}".format(__feature_group__, k): dataset_repr(v)
            for k, v in datasets.items()
        }
    else:
        datasets = {k: dataset_repr(v) for k, v in datasets.items()}
    if filter:
        datasets = {k: v for k, v in datasets.items() if v["kind"] != "unknown"}
    return datasets


@hug.get()
def remove(workspace: String, feature_id: String):
    ws.delete_dataset(workspace, feature_id, group=__feature_group__)


@hug.get()
def rename(workspace: String, feature_id: String, new_name: String):
    ws.rename_dataset(workspace, feature_id, __feature_group__, new_name)


@hug.get()
def group():
    return __feature_group__


@hug.get()
def available():
    h = hug.API(__name__)
    all_features = []
    for name, method in h.http.routes[""].items():
        if name[1:] in ["available", "create", "existing", "remove", "rename", "group"]:
            continue
        name = name[1:]
        func = method["GET"][None].interface.spec
        desc = get_function_api(func)
        category = desc["returns"] or "Others"
        desc = dict(name=name, params=desc["params"], category=category)
        all_features.append(desc)
    return all_features

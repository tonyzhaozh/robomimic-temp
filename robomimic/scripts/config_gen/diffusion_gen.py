from robomimic.scripts.config_gen.helper import *

def make_generator_helper(args):
    algo_name_short = "diffusion_policy"

    generator = get_generator(
        algo_name="diffusion_policy",
        config_file=os.path.join(base_path, 'robomimic/exps/templates/diffusion_policy.json'),
        args=args,
        algo_name_short=algo_name_short,
        pt=True,
    )
    if args.ckpt_mode is None:
        args.ckpt_mode = "off"

    generator.add_param(
        key="train.num_data_workers",
        name="",
        group=-1,
        values=[8],
    )

    generator.add_param(
        key="train.num_epochs",
        name="",
        group=-1,
        values=[1000],
    )

    # use ddim by default
    generator.add_param(
        key="algo.ddim.enabled",
        name="ddim",
        group=1001,
        values=[
            True,
            # False,
        ],
        hidename=True,
    )
    generator.add_param(
        key="algo.ddpm.enabled",
        name="ddpm",
        group=1001,
        values=[
            False,
            # True,
        ],
        hidename=True,
    )

    if args.env == "r2d2":
        generator.add_param(
            key="train.data",
            name="ds",
            group=2,
            values=[
                [{"path": p} for p in scan_datasets("~/Downloads/example_pen_in_cup", postfix="trajectory_im128.h5")],
            ],
            value_names=[
                "pen-in-cup",
            ],
        )
        generator.add_param(
            key="train.action_keys",
            name="ac_keys",
            group=-1,
            values=[
                [
                    "action/abs_pos",
                    "action/abs_rot_6d",
                    "action/gripper_velocity",
                ],
            ],
            value_names=[
                "abs",
            ],
        )
        generator.add_param(
            key="observation.modalities.obs.rgb",
            name="cams",
            group=130,
            values=[
                ["camera/image/hand_camera_image"],
                ["camera/image/hand_camera_image", "camera/image/varied_camera_1_image", "camera/image/varied_camera_2_image"],
            ],
            value_names=[
                "wrist",
                "3cams",
            ]
        )
    elif args.env == "kitchen":
        generator.add_param(
            key="train.data",
            name="ds",
            group=2,
            values=[
                [{"path": "~/datasets/kitchen/prior/human_demos/pnp_table_to_cab/bowls/20230816_im84.hdf5", "filter_key": "100_demos"}],
                # [{"path": "~/datasets/kitchen/prior/human_demos/pnp_table_to_cab/all/20230806_im84.hdf5", "filter_key": "100_demos"}],
                # [{"path": "~/datasets/kitchen/prior/mimicgen/pnp_table_to_cab/viraj_mg_2023-08-10-20-31-14/demo_im84.hdf5", "filter_key": "100_demos"}],
                # [{"path": "~/datasets/kitchen/prior/mimicgen/pnp_table_to_cab/viraj_mg_2023-08-10-20-31-14/demo_im84.hdf5", "filter_key": "1000_demos"}],
            ],
            value_names=[
                "bowls-human-100",
                # "human-100",
                # "mg-100",
                # "mg-1000",
            ],
        )
        
        # update env config to use absolute action control
        generator.add_param(
            key="experiment.env_meta_update_dict",
            name="",
            group=-1,
            values=[
                {"env_kwargs": {"controller_configs": {"control_delta": False}}}
            ],
        )

        generator.add_param(
            key="train.action_keys",
            name="ac_keys",
            group=-1,
            values=[
                [
                    "action_dict/abs_pos",
                    "action_dict/abs_rot_6d",
                    "action_dict/gripper",
                    "action_dict/base_mode",
                    # "actions",
                ],
            ],
            value_names=[
                "abs",
            ],
            hidename=True,
        )
    elif args.env == "square":
        generator.add_param(
            key="train.data",
            name="ds",
            group=2,
            values=[
                [
                    {"path": "~/datasets/square/ph/square_ph_abs_tmp.hdf5"}, # replace with your own path
                ],
            ],
            value_names=[
                "square",
            ],
        )

        # update env config to use absolute action control
        generator.add_param(
            key="experiment.env_meta_update_dict",
            name="",
            group=-1,
            values=[
                {"env_kwargs": {"controller_configs": {"control_delta": False}}}
            ],
        )
        
        generator.add_param(
            key="train.action_keys",
            name="ac_keys",
            group=-1,
            values=[
                [
                    "action_dict/abs_pos",
                    "action_dict/abs_rot_6d",
                    "action_dict/gripper",
                    # "actions",
                ],
            ],
            value_names=[
                "abs",
            ],
        )


    else:
        raise ValueError
    
    generator.add_param(
        key="train.output_dir",
        name="",
        group=-1,
        values=[
            "~/expdata/{env}/{mod}/{algo_name_short}".format(
                env=args.env,
                mod=args.mod,
                algo_name_short=algo_name_short,
            )
        ],
    )

    return generator

if __name__ == "__main__":
    parser = get_argparser()

    args = parser.parse_args()
    make_generator(args, make_generator_helper)
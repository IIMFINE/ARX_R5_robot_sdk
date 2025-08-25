import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import (
    Command,
    FindExecutable,
    PathJoinSubstitution,
    LaunchConfiguration,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def launch_setup(context, *args, **kwargs):
    # Resolve URDF file path
    urdf_path = PathJoinSubstitution(
        [FindPackageShare("arx_r5_controller"), "urdf", LaunchConfiguration("model")]
    ).perform(context)

    # Print URDF file path
    print(f"URDF file path: {urdf_path}")

    # Robot description parameter
    robot_description = Command([FindExecutable(name="xacro"), " ", urdf_path])

    # Nodes
    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        # parameters=[{'robot_description': robot_description}]
        parameters=[
            {"robot_description": ParameterValue(robot_description, value_type=str)}
        ],
        #  launch_ros.parameter_descriptions.ParameterValue(value, value_type=str)
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=[
            "-d",
            PathJoinSubstitution(
                [FindPackageShare("arx_r5_controller"), "rviz_config/rviz2.rviz"]
            ),
        ],
    )

    # Return LaunchDescription
    return [joint_state_publisher_gui_node, robot_state_publisher_node, rviz_node]


def generate_launch_description():
    # Declare arguments
    model_arg = DeclareLaunchArgument(
        name="model", default_value="R5_master.urdf", description="Model argument"
    )
    return LaunchDescription([model_arg, OpaqueFunction(function=launch_setup)])

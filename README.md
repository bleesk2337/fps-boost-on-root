# FPS Automate

## Usage

This script is designed to optimize Android device performance by applying various tweaks and optimizations. It includes the following features:

- Diagnostic information gathering (device model, Android version, CPU, memory, root status)
- Memory cleaning and background process killing
- CPU governor set to "performance" mode
- Thermal throttling control
- Swap file setup (520MB + 956MB)
- Graphics optimizations (disable scissor optimization, set OpenGL 2.0)
- Browser and game cache clearing
- I/O acceleration and MIP control

To use the script, follow these steps:

1. Ensure your Android device is rooted.
2. Copy the `auto_boost.sh` script to your device.
3. Open a terminal on your device and navigate to the script location.
4. Run the script with root permissions: `su -c ./auto_boost.sh`.

The script will perform the various optimizations and log the results to `/sdcard/fps_boost_log.txt`.

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Testing

To test the script, you can run it on a rooted Android device and verify the following:

- The diagnostic information is correctly gathered and logged.
- The memory cleaning and background process killing are effective.
- The CPU governor is set to "performance" mode.
- The thermal throttling control is applied.
- The swap file is correctly set up.
- The graphics optimizations are applied.
- The browser and game caches are cleared.
- The I/O acceleration and MIP control are applied.
- The log file `/sdcard/fps_boost_log.txt` is created and contains the expected output.

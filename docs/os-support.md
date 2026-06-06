# OS Support Mapping

Samaj tracks OS compatibility as catalog metadata only. OS mapping does not
mean a tool is installed, supported, tested, safe, recommended, executable, or
permitted to use.

## Supported Metadata Fields

- `windows_supported`
- `kali_supported`
- `linux_supported`
- `mac_supported`
- `install_method_windows`
- `install_method_kali`
- `install_method_linux`
- `requires_admin_or_root`
- `requires_network`
- `requires_api_key`
- `adapter_available`

The default value for OS support is `unknown`.

## Detection Foundation

`samaj/core/os_detect.py` detects:

- Windows
- Kali Linux
- Debian Linux
- Ubuntu Linux
- Other Linux
- Unknown OS

`samaj/core/environment.py` reports the current OS, Python executable, Python
version, and whether a virtual environment is active.

## Anti-Hallucination Rule

Do not infer support from a tool name. A future developer must verify support
and update the catalog entry explicitly.

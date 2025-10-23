# kishash
CLI tool to generate and validate 'hash.hex' files that contain an embedded secret key.

## Quick usage (examples)

### Generate a file:
```sh
python hashcli.py generate
```

#### Output:
```sh
✅ File 'hash.hex' written successfully.
🔑 Generated secret key: a1b2c3d4e5
```

### Validate / extract key:
```sh
python hashcli.py validate
```

#### Output:
```sh
🔍 Extracted key: a1b2c3d4e5
ℹ️ No key provided for comparison. Extraction finished.
```

### Validate and compare with a known key:
```sh
python hashcli.py validate --key a1b2c3d4e5
```
#### Output will indicate whether the provided key matches.

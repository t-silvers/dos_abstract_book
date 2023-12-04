# DoS Booklet-Maker

## Set-up

### Cloning the repository

Clone the repository using:

```bash
git clone
```

### Required executables

The following executables are required:

- `make`
- `python`
- `rclone`

Their locations can be specified in the `Makefile` using the variables `PYTHON` and `RCLONE`, respectively.

### Installing `rclone`

Follow the instructions [here](https://rclone.org/downloads/) if working in an environment without an `rclone` installation. If working on the cluster, there is no need to install `rclone`.

Otherwise, if working on a private computer, script download and installation of `rclone` may be run on Linux/macOS/BSD systems using:

```bash
sudo -v ; curl https://rclone.org/install.sh | sudo bash
```

### Configuring `rclone` remote

Run `rclone config` and [follow the instructions](https://rclone.org/drive/) to configure `rclone` for your Google Drive account. The default configuration name is `remote`.

### Typesetting LaTeX

The booklet is typeset using TexpadTex, a lightweight typesetter bundled with [Texifier](https://www.texifier.com), but should be compatible with most LaTeX typesetters, including latexmk or pdfLaTex, the default typesetter in Overleaf.

## Usage

### Generating the booklet

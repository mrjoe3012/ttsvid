# ttsvid

This application uses XTTS to convert input strings into realistic, presenter-style commentary.

## Installation and Usage

Ensure you have Python version 3 installed before attempting the steps below.

The easiest way to install the application is by using the pre-packaged wheel file. Download the latest release [here](https://github.com/mrjoe3012/ttsvid/releases/download/v1.0/ttsvid-1.0-py3-none-any.whl).

Once the wheel file has been downloaded, open a terminal in the directory it has been downloaded to and run the following command:

```bash
pip install <the wheel file>
```

For now, you will need the source code to run the program as it depends on the `presenter.mp3` file. Use git or download this repository as a zip file and extract it. Navigate into the directory and run 

```bash
ttsvid "this is one quote" "here is another"
```

After a few minutes `output.mp3` should contain the required voice commentary.

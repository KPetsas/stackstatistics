# Stackstatistics

Stackstatistics is a simple CLI application that retrieves data from the StackExchange API and calculates some simple statistics.

## Getting Started - Installation

These instructions will help you with the system set up needed for the application to be installed on your local machine.

### Prerequisites

Before we get started, ensure you have python version 2.7.x installed, in order to proceed.

- For Linux Debian-based operating systems:
  1) Open a terminal window.
  2) Navigate to the application's root directory, which contains the **system-setup.sh** file.
  3) Execute the script by running the following command:
```
$ . system-setup.sh
```
**or**
```
$ /bin/sh system-setup.sh
```
**or** if it fails run the following commands (manual system configuration):
```
# install the python-pip package
sudo apt-get -y --force-yes install software-properties-common
sudo apt-add-repository universe
sudo apt-get update
sudo apt-get -y install python-pip

# Install python-dev package
sudo apt-get install python-dev
```
*Note: omit **sudo** in the above commands if you are root user.*

The application makes use of the Python packages listed below:
- `requests` - Useful for making HTTP requests
- `tabulate` - Helps in printing the application's ouput in tabular format
- `flask-table` - Helps in printing the application's ouput in HTML format
- `pytest` - This is the testing framework of the application

If you configure the system manually (without using the **system-setup.sh** script) you can install each package with `pip` **or** navigate to the folder containing the **requirements.txt** file and run the command:
```
# Install all the required python packages
sudo pip install -r requirements.txt
```
*Note: omit **sudo** in the above commands if you are root user.*

- For any other operating system follow the same logic:
  1) Open a command window.
  2) Install the python-pip package.
  3) Navigate to the application folder containing the **requirements.txt** file.
  4) Install the requirements included in the corresponding file with the `pip install` command.

### Installing the application

By following the next steps you can install the stackstatistics application on your local machine. Firstly, open a command line window and navigate to the application folder containing the **setup.py** file. Run the command:
```
$ sudo python setup.py install
```
*Note: omit **sudo** in the above command if you are root user.*

Finally, run the below command to assure the success of the installation.
```
$ statistics -h
```
You should now see a help message on how to use the application.

## How to run the application

To run the application follow the below command structure.
```
$ statistics "arguments"
```

Required arguments for statistics command:
```
--since "date"
--until "date"
```
where **date** has the format: YYYY-MM-DD HH:MM:SS

For example:
```
--since "2017-4-12 10:00:00"
--until "2017-4-12 11:00:00"
```

Optional arguments for statistics command:
```
--output-format format
```
where **format** is one of "**tabular** | **JSON** | **HTML** (case insensitive - default value: tabular)"

For instance:
```
--output-format json
```

### Example

This is a complete example on how to run the application.
```
$ statistics --since "2017-6-2 10:00:00" --until "2017-6-3 12:02:00" --output-format HTML
```

## Running the tests

To ensure the application has the expected functionality, you could run the unit tests written for this purpose. To proceed follow the steps described below.

- Open a command line window.
- Navigate to the application's root directory (which is the location/path that contains this [README.md](README.md) file).
- To run all the tests execute the command:

```
$ py.test
```


## Authors

* **Konstantinos Petsas** - *Initial work* -

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


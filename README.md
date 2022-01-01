What This Project Does:
        This project was built to be able to track and visualize the level of water in a water tank in my basement. 

Data Collection:
        The water level is found using an ultra-sonic sensor mounted to the top of the tank. The height of the water (and thus how much water the tank is holding), can be calculated by how long it takes for an ultrasonic sound signal to leave, bounce of the surface of the water, and come back. A measurement is taken every minute.
        
Data Storage:
        The data is stored in MariaDB. Each entry stores a water level reading and a timestamp. Only the data from the past 30 days in stored. Any older data is automatically deleted.

Reading the Data:
        The data can be viewed in two ways: a website on the local network, and in a daily email.

Website:
        The website is generated with a cgi script that calls python functions to query the database for the current water level and a function to generated a new up to date graph of water level vs time.
        
Email:
        An email is sent out every day at 6:00pm. This email displays the current water level as well as how much water was used and how much water was brought in over the last 24 hours. Before the water usage can be accurately calulated, noise must be removed from the sensor data. I wrote a noise removal function specifically tailored to the type of data received from a system like this.

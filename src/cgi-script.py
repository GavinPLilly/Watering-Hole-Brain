# Module imports

# My imports
import get_prop
import database_wrapper
import data_comp_wrapper

CHART_FILE  = get_prop.get_prop("CHART_FILE", "s") + ".png"

recent_level, recent_time = database_wrapper.get_newest_entry()

print("""\
Content-type: text/html
<body>
    <head>
        <title>Watering Hole Brain</title>
        <style>
            h1 {
                display: flex;
                justify-content: center;
                align-items: center;
            }
            p {
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .image {
                display: flex;
                justify-content: center;
                align-items: center;
            }
        <\style>
    </head>

    <h1>Watering Hole Brain</h1>
    <p>The Well Manager is at """ + str(recent_level) + """</p>

    <div class="image">
        <img src=\"""" + str(CHART_FILE) + """\" alt="Water Chart" height="500px">
    </div>

    <p>Updated at """ + str(recent_time) + """</p>
</body>
""")

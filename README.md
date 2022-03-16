# US-Research-Assessment
Quick Access Dataset Notesheet
<ol>
Confidential Information:
<li>Q1: 1i confidential (probably animal research space?)</li>
<li>Q3: Amount of research animal space - not included (no big deal)</li>
<li>Q7: Condition of research NASF</li>
<li>Q10: NASF research animal space</li>
</ol>
<ol>
Abbreviations:
<li>R/R -> Repair and Renovation</li>
<li>NASF -> Net Assignable Square Feet</li>
<li>S&E -> Science & Engineering</li>
<li>R&D -> Research & Development</li>
</ol>
<ul>
Necessary Modules:
<li> Pandas</li>
<li> Geopandas</li>
<li> Matplotlib</li>
<li> Pathlib</li>
<li> os path</li>
<li> cse163_utils (for test file)</li>
</ul>
<ul>
Coding issues to watch out for:
<li>The CSVs are encoded in ISO-8859-1, so anytime you call ‘read_csv’ you must put the argument <code>encoding='ISO-8859-1</code></li>
<li>This is also in a comment in sanitize_data.py, but the flake8-neccessitated formatting makes a little unclear.<br />
To call sanitize_data.py, use the following syntax in your command line of choice:<br />
<code>[python executable] [path of sanitize_data.py] [path of raw_data directory] [path of location directory] [year]</code><br />
For example:<br />
<code>python ./src/sanitize_data.py ./raw_data/ ./data/ '2007:2019'</code></li>
</ul>
<ul>
-Running data_analysis and func_tests: <br>
It should be possible to run both data_analysis and funct_tests without any additional inputs.</br></li>
<li>Run the python executable in command line or a text editor
<li>If issues with the directories arise, double-check that the "path" and "geopath" variables point to the correct files</li>
<li>The path variable should point to the desired year(s) of data (ex. 2007-2019_sanitized.csv)</li>
<li>Similarly, the path_2007 and path_2019 variables in funct_tests are the two years being tested, and may be any year's data file</li>
<li>The geopath variable should point to the geodata (should always be state_geodata.json)</li>
<li>If pictures are not saving properly, check where pics_dir is saving to</li>
<li>The pics_dir variable should point to where you want to send the output figures</li>
</ul>
<ul>
Data file naming conventions:
<li>Raw data is named in the form: "facilities_[year].csv", and is stored in the subdirectory "raw_data". They must be compiled with sanitize_data before use</li>
<li>Note that the year in the file name is the <b>fiscal year</b> so ex. the file for 2019 is actually data from 2018</li>
<li>sanitize_data will output files into the desired location with the desired naming; for best results, be consistent with naming conventions and especially be consistent with using the same target directory</li>
<li>In the program authors' version of the code, the data was stored in folder "data" and used the naming convention "[start year]-[end year]_sanitized.csv"</li>
<ul>

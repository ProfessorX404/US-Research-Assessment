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
Coding issues to watch out for:
<li>The CSVs are encoded in ISO-8859-1, so anytime you call ‘read_csv’ you must put the argument <code>encoding='ISO-8859-1</code></li>
<li>This is also in a comment in sanitize_data.py, but the flake8-neccessitated formatting makes a little unclear.<br />
To call sanitize_data.py, use the following syntax in your command line of choice:<br />
<code>[python executable] [path of sanitize_data.py] [path of desired CSV to sanitize] [path of desired location and name of CSV] [year]</code><br />
For example:<br />
<code>./.env/python.exe ./src/sanitize_data.py ./raw_data/facilities_2019_imputed.csv ./data/2019_sanitized.csv 2019</code></li>
</ul>

from flask import Flask, render_template, request
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ============================================================
# FOLDERS
# ============================================================

SUBMISSIONS_FOLDER = "submissions"
UPLOADS_FOLDER = os.path.join(SUBMISSIONS_FOLDER, "uploads")

os.makedirs(SUBMISSIONS_FOLDER, exist_ok=True)
os.makedirs(UPLOADS_FOLDER, exist_ok=True)


# ============================================================
# REFERENCE NUMBER
# ============================================================

def create_reference():
    return "CSR-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3]


# ============================================================
# MAIN PAGES
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/report")
def report():
    return render_template("report.html")


# ============================================================
# CRIME CATEGORY PAGES
# ============================================================

@app.route("/theft")
def theft():
    return render_template("theft.html")


@app.route("/burglary")
def burglary():
    return render_template("burglary.html")


@app.route("/robbery")
def robbery():
    return render_template("robbery.html")


@app.route("/assault")
def assault():
    return render_template("assault.html")


@app.route("/sexual-offence")
def sexual_offence():
    return render_template("sexual-offence.html")


@app.route("/vehicle-crime")
def vehicle_crime():
    return render_template("vehicle_crime.html")


@app.route("/fraud-scam")
def fraud_scam():
    return render_template("fraud_scam.html")


@app.route("/vandalism")
def vandalism():
    return render_template("vandalism.html")


@app.route("/murder")
def murder():
    return render_template("murder.html")


@app.route("/drug-illegal-activity")
def drug_illegal_activity():
    return render_template("drug_illegal_activity.html")


@app.route("/other-crime")
def other_crime():
    return render_template("other_crime.html")


# ============================================================
# HELPER FUNCTION - SAVE EVIDENCE
# ============================================================

def save_evidence(category, timestamp, report_filepath):

    evidence = request.files.get("evidence")

    if evidence and evidence.filename:

        original_filename = secure_filename(evidence.filename)

        if original_filename:

            safe_category = secure_filename(
                category.lower()
                .replace("/", "_")
                .replace(" ", "_")
            )

            evidence_filename = (
                f"{safe_category}_{timestamp}_{original_filename}"
            )

            evidence_filepath = os.path.join(
                UPLOADS_FOLDER,
                evidence_filename
            )

            evidence.save(evidence_filepath)

            with open(report_filepath, "a", encoding="utf-8") as file:
                file.write(
                    f"Evidence file: uploads/{evidence_filename}\n"
                )

            return evidence_filename

    return None


# ============================================================
# THEFT SUBMISSION
# ============================================================

@app.route("/submit-theft", methods=["POST"])
def submit_theft():

    date = request.form.get("date")
    time = request.form.get("time")
    location = request.form.get("location")
    items = request.form.get("items")
    value = request.form.get("value")
    description = request.form.get("description")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    reference = create_reference()

    filename = f"theft_{timestamp}.txt"
    filepath = os.path.join(SUBMISSIONS_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as file:

        file.write("CRIME SPOT REPORTER - THEFT REPORT\n")
        file.write("----------------------------------\n")
        file.write(f"Reference Number: {reference}\n")
        file.write(f"Date: {date}\n")
        file.write(f"Time: {time}\n")
        file.write(f"Location: {location}\n")
        file.write(f"Items stolen: {items}\n")
        file.write(f"Estimated value: R{value}\n")
        file.write(f"Additional information: {description}\n")

    save_evidence("Theft", timestamp, filepath)

    return confirmation("Theft", reference)


# ============================================================
# BURGLARY SUBMISSION
# ============================================================

@app.route("/submit-burglary", methods=["POST"])
def submit_burglary():

    date = request.form.get("date")
    time = request.form.get("time")
    location = request.form.get("location")
    property_type = request.form.get("property")
    entry = request.form.get("entry")
    stolen = request.form.get("stolen")
    suspect = request.form.get("suspect")
    description = request.form.get("description")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    reference = create_reference()

    filename = f"burglary_{timestamp}.txt"
    filepath = os.path.join(SUBMISSIONS_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as file:

        file.write(
            "CRIME SPOT REPORTER - HOUSEBREAKING / BURGLARY REPORT\n"
        )
        file.write(
            "------------------------------------------------------\n"
        )
        file.write(f"Reference Number: {reference}\n")
        file.write(f"Date: {date}\n")
        file.write(f"Time: {time}\n")
        file.write(f"Location: {location}\n")
        file.write(f"Property type: {property_type}\n")
        file.write(f"How entry was gained: {entry}\n")
        file.write(f"Stolen or damaged property: {stolen}\n")
        file.write(f"Suspect information: {suspect}\n")
        file.write(f"Additional information: {description}\n")

    save_evidence("Burglary", timestamp, filepath)

    return confirmation("Housebreaking / Burglary", reference)


# ============================================================
# ROBBERY SUBMISSION
# ============================================================

@app.route("/submit-robbery", methods=["POST"])
def submit_robbery():

    date = request.form.get("date")
    time = request.form.get("time")
    location = request.form.get("location")
    weapon = request.form.get("weapon")
    items = request.form.get("items")
    suspect = request.form.get("suspect")
    description = request.form.get("description")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    reference = create_reference()

    filename = f"robbery_{timestamp}.txt"
    filepath = os.path.join(SUBMISSIONS_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as file:

        file.write("CRIME SPOT REPORTER - ROBBERY REPORT\n")
        file.write("-----------------------------------\n")
        file.write(f"Reference Number: {reference}\n")
        file.write(f"Date: {date}\n")
        file.write(f"Time: {time}\n")
        file.write(f"Location: {location}\n")
        file.write(f"Was a weapon used?: {weapon}\n")
        file.write(f"Items or property taken: {items}\n")
        file.write(f"Suspect description: {suspect}\n")
        file.write(f"Additional information: {description}\n")

    save_evidence("Robbery", timestamp, filepath)

    return confirmation("Robbery", reference)


# ============================================================
# ASSAULT SUBMISSION
# ============================================================

@app.route("/submit-assault", methods=["POST"])
def submit_assault():

    date = request.form.get("date")
    time = request.form.get("time")
    location = request.form.get("location")
    injuries = request.form.get("injuries")
    weapon = request.form.get("weapon")
    suspect = request.form.get("suspect")
    description = request.form.get("description")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    reference = create_reference()

    filename = f"assault_{timestamp}.txt"
    filepath = os.path.join(SUBMISSIONS_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as file:

        file.write("CRIME SPOT REPORTER - ASSAULT REPORT\n")
        file.write("-----------------------------------\n")
        file.write(f"Reference Number: {reference}\n")
        file.write(f"Date: {date}\n")
        file.write(f"Time: {time}\n")
        file.write(f"Location: {location}\n")
        file.write(f"Were there injuries?: {injuries}\n")
        file.write(f"Was a weapon involved?: {weapon}\n")
        file.write(f"Suspect description: {suspect}\n")
        file.write(f"Description of incident: {description}\n")

    save_evidence("Assault", timestamp, filepath)

    return confirmation("Assault", reference)


# ============================================================
# SEXUAL OFFENCE SUBMISSION
# ============================================================

@app.route("/submit-sexual-offence", methods=["POST"])
def submit_sexual_offence():

    date = request.form.get("date")
    time = request.form.get("time")
    location = request.form.get("location")
    description = request.form.get("description")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    reference = create_reference()

    filename = f"sexual_offence_{timestamp}.txt"
    filepath = os.path.join(SUBMISSIONS_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as file:

        file.write(
            "CRIME SPOT REPORTER - SEXUAL OFFENCE REPORT\n"
        )
        file.write("--------------------------------------------\n")
        file.write(f"Reference Number: {reference}\n")
        file.write(f"Date: {date}\n")
        file.write(f"Time: {time}\n")
        file.write(f"Location: {location}\n")
        file.write(f"Description: {description}\n")

    save_evidence("Sexual Offence", timestamp, filepath)

    return confirmation("Sexual Offence", reference)


# ============================================================
# NEW CATEGORY SUBMISSIONS
# ============================================================

@app.route("/submit", methods=["POST"])
def submit():

    category = request.form.get(
        "crime_category",
        "Other Crime"
    )

    date = request.form.get("date")
    time = request.form.get("time")
    location = request.form.get("location")
    description = request.form.get("description")

    safe_category = secure_filename(
        category.lower()
        .replace("/", "_")
        .replace(" ", "_")
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    reference = create_reference()

    report_filename = (
        f"{safe_category}_{timestamp}.txt"
    )

    report_filepath = os.path.join(
        SUBMISSIONS_FOLDER,
        report_filename
    )

    with open(report_filepath, "w", encoding="utf-8") as file:

        file.write(
            "CRIME SPOT REPORTER - CRIME REPORT\n"
        )
        file.write("---------------------------------\n")
        file.write(f"Reference Number: {reference}\n")
        file.write(f"Crime category: {category}\n")
        file.write(f"Date: {date}\n")
        file.write(f"Time: {time}\n")
        file.write(f"Location: {location}\n")
        file.write(f"Description: {description}\n")

    save_evidence(
        category,
        timestamp,
        report_filepath
    )

    return confirmation(category, reference)


# ============================================================
# CONFIRMATION PAGE WITH SHARE REFERENCE
# ============================================================

def confirmation(category, reference):

    return f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <title>
            Report Submitted - Crime Spot Reporter
        </title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 40px 20px;
                text-align: center;
                background: #f5f5f5;
            }}

            main {{
                max-width: 600px;
                margin: auto;
                background: white;
                padding: 40px 25px;
                border-radius: 12px;
                box-shadow:
                    0 4px 15px rgba(0, 0, 0, 0.1);
            }}

            h1 {{
                margin-bottom: 20px;
            }}

            .reference {{
                font-size: 24px;
                font-weight: bold;
                margin: 25px 0;
                padding: 15px;
                border: 2px solid #222;
                border-radius: 8px;
                background: #f8f8f8;
                word-break: break-word;
            }}

            button {{
                padding: 12px 20px;
                margin: 8px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 15px;
            }}

        </style>

    </head>

    <body>

        <main>

            <h1>
                Report Submitted Successfully
            </h1>

            <p>
                Your
                <strong>{category}</strong>
                report has been recorded.
            </p>

            <p>
                Your report reference number is:
            </p>

            <div class="reference">
                {reference}
            </div>

            <p>
                Please keep this reference number
                for your records.
            </p>

            <p>
                Thank you for helping keep
                your community safe.
            </p>

            <br>

            <button
                onclick="window.location.href='/'"
            >
                Return to Crime Spot Reporter
            </button>

            <button
                onclick="window.location.href='/report'"
            >
                Report Another Crime
            </button>

            <button
                onclick="shareReference()"
            >
                Share Reference
            </button>

        </main>

        <script>

            function shareReference() {{

                const reference = "{reference}";
                const category = "{category}";

                const message =
                    "Crime Spot Reporter\\n" +
                    "Report category: " + category + "\\n" +
                    "Reference number: " + reference;

                if (navigator.share) {{

                    navigator.share({{
                        title: "Crime Spot Reporter",
                        text: message
                    }}).catch(function(error) {{
                        console.log(
                            "Sharing cancelled or unavailable:",
                            error
                        );
                    }});

                }} else {{

                    navigator.clipboard.writeText(message)
                        .then(function() {{

                            alert(
                                "Reference copied to clipboard."
                            );

                        }})
                        .catch(function() {{

                            alert(
                                "Your reference number is: " +
                                reference
                            );

                        }});

                }}
            }}

        </script>

    </body>

    </html>
    """


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)


function startReport() {
    window.location.href = "/report";
}

function toggleMenu() {
    alert("Menu button is working!");
}

function selectCrimeCategory(category) {

    if (category === "Theft") {
        window.location.href = "/theft";
    }
    else if (category === "Housebreaking / Burglary") {
        window.location.href = "/burglary";
    }
    else if (category === "Robbery") {
        window.location.href = "/robbery";
    }
    else if (category === "Assault") {
        window.location.href = "/assault";
    }
    else if (category === "Sexual Offence") {
        window.location.href = "/sexual-offence";
    }
    else if (category === "Vehicle Crime") {
        window.location.href = "/vehicle-crime";
    }
    else if (category === "Fraud / Scam") {
        window.location.href = "/fraud-scam";
    }
    else if (category === "Vandalism / Property Damage") {
        window.location.href = "/vandalism";
    }
    else if (category === "Murder / Attempted Murder") {
        window.location.href = "/murder";
    }
    else if (category === "Drug / Illegal Activity") {
        window.location.href = "/drug-illegal-activity";
    }
    else if (category === "Other Crime") {
        window.location.href = "/other-crime";
    }
}

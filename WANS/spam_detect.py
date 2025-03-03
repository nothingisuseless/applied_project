## ************************************GROUP 6 ASSIGNMENT************************************************
## ************************************CHAKRAVORTY DEVOPRIYA DEVASHISH************************************************
## ************************************SUMIT MUKHERJEE****************************************************************
## ************************************SOUAGATA DUTTA*****************************************************************
## ************************************VINEET SINHA*******************************************************************
## ************************************VIJAY KUMAR********************************************************************
## ************************************SUNIL SINGH********************************************************************


import dns.resolver  # Import the DNS resolver from the 'dnspython' library for querying DNS records.
import smtplib  # Import the 'smtplib' library for sending email and handling SMTP operations.
import socket  # Import the 'socket' library for handling network-related operations, like timeouts.
import ssl  # Import the 'ssl' library for managing TLS/SSL connections.

# Function to check SPF records for a given domain.
def check_spf(domain):
    try:
        # Query DNS for TXT records of the domain.
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            # Look for SPF records, which start with "v=spf1".
            if rdata.to_text().startswith('"v=spf1'):
                score = 20  # Start with a base score of 20 if an SPF record is found.
                # Check for strict SPF policy (-all) which blocks all non-authorized senders.
                if "-all" in rdata.to_text():
                    score += 5  # Add 5 points for strict SPF policy.
                # Return score and description of SPF record.
                return score, "SPF record found with strict policy." if "-all" in rdata.to_text() else "SPF record found."
    except:
        pass  # If there's an error, return a score of 0.
    return 0, "No valid SPF record found."  # Return 0 if no SPF record is found.

# Function to check DKIM records for a given domain.
def check_dkim(domain):
    # List of common DKIM selectors.
    selectors = ['default', 'selector1', 'selector2']
    resolver = dns.resolver.Resolver()  # Create a DNS resolver instance.
    resolver.timeout = 10  # Set DNS query timeout to 10 seconds.
    resolver.lifetime = 10  # Set DNS query lifetime to 10 seconds.
    resolver.nameservers = ['8.8.8.8', '1.1.1.1']  # Use Google's and Cloudflare's DNS servers.

    for selector in selectors:
        try:
            # Construct the DKIM domain using the selector and the domain.
            dkim_domain = f"{selector}._domainkey.{domain}"
            # Query DNS for TXT records associated with the DKIM domain.
            answers = resolver.resolve(dkim_domain, 'TXT')
            for rdata in answers:
                # Check for DKIM records, which start with "v=DKIM1".
                if 'v=DKIM1' in rdata.to_text():
                    return 20, f"DKIM record found with selector '{selector}'."  # Return score if DKIM is found.
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers, dns.resolver.LifetimeTimeout):
            continue  # Move to the next selector if no record is found or if there's a timeout.
    return 0, "No valid DKIM record found or the query timed out."  # Return 0 if no DKIM record is found.

# Function to check DMARC records for a given domain.
def check_dmarc(domain):
    try:
        # Construct the DMARC domain.
        dmarc_domain = f"_dmarc.{domain}"
        # Query DNS for TXT records associated with the DMARC domain.
        answers = dns.resolver.resolve(dmarc_domain, 'TXT')
        for rdata in answers:
            # Check for DMARC records, which start with "v=DMARC1".
            if 'v=DMARC1' in rdata.to_text():
                score = 20  # Start with a base score of 20 if a DMARC record is found.
                # Check the policy specified in the DMARC record.
                policy = rdata.to_text().split(';')[1].strip()
                if 'p=reject' in policy:
                    score += 5  # Add 5 points for a strict 'reject' policy.
                    return score, "DMARC record found with 'reject' policy."
                elif 'p=quarantine' in policy:
                    score += 3  # Add 3 points for a 'quarantine' policy.
                    return score, "DMARC record found with 'quarantine' policy."
                elif 'p=none' in policy:
                    score += 1  # Add 1 point for a 'none' policy.
                    return score, "DMARC record found with 'none' policy."
    except:
        pass  # If there's an error, return a score of 0.
    return 0, "No valid DMARC record found."  # Return 0 if no DMARC record is found.

# Function to check if the domain supports TLS on a given port (default: 587).
def check_tls(domain, port=587):
    try:
        context = ssl.create_default_context()  # Create a default SSL context.

        # Establish an SMTP connection to the domain on the specified port.
        with smtplib.SMTP(domain, port, timeout=10) as server:
            server.ehlo()  # Identify the client to the SMTP server.
            starttls_response = server.starttls(context=context)  # Attempt to start TLS.
            server.ehlo()  # Re-identify after starting TLS.

            # Check if TLS was successfully started (220 response code).
            if starttls_response[0] == 220:
                return 10, f"TLS is supported on {domain}:{port}. Connection secured."
            else:
                return 0, f"TLS is not supported on {domain}:{port}. StartTLS response: {starttls_response}"

    except (smtplib.SMTPException, socket.timeout, ssl.SSLError, ConnectionRefusedError) as e:
        # Handle any exceptions related to SMTP, timeouts, SSL, or connection errors.
        return 0, f"Failed to connect or initiate TLS on {domain}:{port}. Error: {str(e)}"

# Function to check if the domain's SMTP server is an open relay.
def check_open_relay(domain):
    try:
        test_email = "test@example.com"  # A placeholder email address for testing.
        with smtplib.SMTP(domain, 25) as server:
            server.mail("test@example.com")  # Identify the sender.
            code, _ = server.rcpt(test_email)  # Attempt to send to the recipient.
            if code == 250:
                return -30, "The server is an open relay."  # Return a negative score if the server is an open relay.
    except:
        pass  # If there's an error, assume the server is not an open relay.
    return 0, "The server is not an open relay."  # Return 0 if the server is not an open relay.

# Function to assess the overall email security of a given domain.
def assess_email_security(domain):
    score = 0  # Initialize the score to 0.
    results = []  # Initialize an empty list to store the results.

    # Check SPF records and update the score and results.
    spf_score, spf_result = check_spf(domain)
    score += spf_score
    results.append(spf_result)

    # Check DKIM records and update the score and results.
    dkim_score, dkim_result = check_dkim(domain)
    score += dkim_score
    results.append(dkim_result)

    # Check DMARC records and update the score and results.
    dmarc_score, dmarc_result = check_dmarc(domain)
    score += dmarc_score
    results.append(dmarc_result)

    # Check TLS support and update the score and results.
    tls_score, tls_result = check_tls(domain)
    score += tls_score
    results.append(tls_result)

    # Check for open relay and update the score and results.
    open_relay_score, open_relay_result = check_open_relay(domain)
    score += open_relay_score
    results.append(open_relay_result)

    # Adjust the final score based on the total assessment.
    if score >= 85:
        score += 5  # Reward for high scores.
    elif score <= 50:
        score -= 5  # Penalty for low scores.

    score = max(1, min(100, score))  # Ensure the score is between 1 and 100.
    return score, results  # Return the final score and results.

# Example usage of the script.
if __name__ == "__main__":
    domain = ""  # Replace with your domain
    score, results = assess_email_security(domain)
    print(f"The security score for {domain} is: {score}\n")
    for result in results:
        print(result)

# CosmoFlow

This project is designed to be the "Final Boss" of your course. 

It is a monolithic project that requires you to build a complete scientific pipeline: from generating raw data, to optimizing analysis code, to serving it to a user.

------------------------------------------------------------------------------------------------------------------------------------------

Project Title: "CosmoFlow: The End-to-End Survey Simulator"
The Concept:You will build a full-stack system that generates a mock galaxy redshift survey (like DESI or Euclid), calculates clustering statistics using high-performance code, and visualizes the results on an interactive web dashboard.

------------------------------------------------------------------------------------------------------------------------------------------

Phase 1: The Core Python Package (src/cosmoflow)
Goal: Build the engine that generates the data.
Syllabus Covered: Packaging, OOP, Testing, Docs, Git.
The Structure: Set up a professional pyproject.toml structure.
Polymorphism (OOP): Create a base class Tracer with subclasses LuminousRedGalaxy and EmissionLineGalaxy.
Each subclass has different bias parameters and luminosity_functions.
Implement a method .generate_redshifts(n) that returns mock data based on these specific physics.
Documentation (Sphinx): Document the luminosity functions using LaTeX math. Explain the physical difference between your galaxy classes.
Testing (Pytest): Write tests to ensure your random distributions follow expected statistical properties (e.g., "The mean redshift of LRGs should be approx 0.8").

------------------------------------------------------------------------------------------------------------------------------------------

Phase 2: High-Performance Analysis Engine
Goal: Analyze the generated data, focusing on speed and complexity.
Syllabus Covered: Computing in Python, Multi-language (Cython), Complexity/Big O, Profiling.
The Task: Implement the 2-Point Correlation Function, $\xi(r)$. This counts pairs of galaxies at separation $r$.
The Baseline: Write a pure Python version (nested loops). It will be $O(N^2)$ and slow.
The Optimization:
Numpy: Vectorize the distance calculation.
Cython: Write a compiled module _pair_counter.pyx to handle the heavy number crunching.
Benchmark: Create a plot showing the execution time of Python vs. Cython for $N=100, 1k, 10k$. Prove the performance gain.
Integration: Expose this optimized function in your main package: cosmoflow.compute_xi(data).

------------------------------------------------------------------------------------------------------------------------------------------

Phase 3: The Command Line Interface (CLI)
Goal: Allow "batch processing" of simulations.Syllabus Covered: Environments (Conda), CLI Tools, Logging, Error Handling.
The Tool: Create a command cosmo-gen using argparse.Bashcosmo-gen --type LRG --count 50000 --output survey_data.json
Error Handling: If the user requests a negative number of galaxies or an unknown galaxy type, raise a custom ConfigurationError and log it gracefully.
Environment: Create an environment.yml that locks the versions of Numpy, Cython, and your other tools.

------------------------------------------------------------------------------------------------------------------------------------------

Phase 4: Full-Stack Visualization
Goal: Make the data accessible via a web browser.
Syllabus Covered: FastAPI, Next.js, Deployment (Docker).
Backend (FastAPI):
Endpoint 1: GET /generate triggers the simulation engine.
Endpoint 2: POST /analyze accepts the galaxy data and runs your Cython-optimized $\xi(r)$ calculator.
Use Pydantic to strictly define the JSON schema for a "Galaxy."
Frontend (Next.js):
Visual 1: A "Cone Plot" (Polar projection) showing the 3D distribution of the generated galaxies.
Visual 2: A line graph of the Correlation Function $\xi(r)$ returned by the backend.
Controls: Sliders to change the number of galaxies or the cosmology parameters.
Deployment: Write a docker-compose.yml file.
Service A: The FastAPI backend (installing your compiled Cython package inside the Docker container).
Service B: The Next.js frontend.One command (docker-compose up) should launch the whole laboratory.

------------------------------------------------------------------------------------------------------------------------------------------

Phase 5: Professional DevOpsGoal: Automate maintenance.
Syllabus Covered: Continuous Integration (GitHub Actions), PyPI Distribution.
CI Pipeline:
On every push: Run pytest.
On every push: Compile the Cython extension to check for build errors.
On every push: Build the Sphinx docs.
Distribution: Configure the pipeline to build a binary wheel (.whl) of your package (which includes the compiled C-extensions) so it can be installed on other machines.

------------------------------------------------------------------------------------------------------------------------------------------

Summary of the "CosmoFlow" Architecture

| Component      | Syllabus Modules | Cosmology Task                                     |
|:---------------|:-----------------|:---------------------------------------------------|
| src/cosmoflow  | 5, 6, 7, 12, 13  | OOP Galaxy Generators, Cython Correlation Function |
| tests/         | 10               | Verify statistical properties of mock              |
| datadocs/      | 8                | LaTeX explanations of $\xi(r)$ and bias            |
| cli.py         | 1, 2, 9, 11      | Command line tool to run simulations               |
| api/ (FastAPI) | 14               | HTTP wrapper around the Python package             |
| web/ (Next.js) | 15               | Interactive Cone Plot & Data Dashboard             |
| .github/       | 4, 17            | CI/CD actions for testing and building             |
| Dockerfile     | 16               | Containerizing the complex Cython build            |

------------------------------------------------------------------------------------------------------------------------------------------

This project forces you to connect the "heavy math" (Cython/Numpy) with the "modern web" (FastAPI/React), bridging the gap between a Researcher and a Software Engineer.
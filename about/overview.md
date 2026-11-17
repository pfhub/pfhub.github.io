# About PFHub

# Primary PFHub Goals

1. Provide a set of benchmark problems to compare and contrast codes for solving phase field equations.
2. Provide quality assurance for phase field codes based on performance and accuracy.
3. Increase the adoption of phase field methods in engineering and academic applications with the development of practical documentation.
4. Foster an engaged and integrated phase field community.

# Details and mentions

- Olle Heinonen wrote a philosophical introduction to the PFHub benchmarking effort, available as an [extended essay](essay)
- [Andrea Jokisaari][Andrea], [Peter Voorhees][Peter], [Jon Guyer][Jon], [Jim Warren][Jim] and [Olle Heinonen][Olle] published a peer-reviewed journal article in Computational Materials Science entitled [“Benchmark problems for numerical implementations of phase field models”][benchmark journal].
    - CHiMaD News posted an overview of the article entitled  [“Benchmark Problems for Phase Field Methods”][benchmark news].
- Aashutosh Mistry wrote an overview of the presentation delivered by [Jon Guyer][Jon] at MRS 2017 entitled [“Benchmarking Problems for Phase Field Codes”][benchmark overview].

# Get Involved

We are an inclusive and expanding community and welcome new participants. All those interested in phase field modeling are welcome to participate in a variety of different ways. See the [involvement guide][involvement guide] for more details about how you can get involved with the community.

# Community

Please see the [community page][community page] for details of individuals involved in this project and their affiliations.

# Suggested Phase Field Codes

The goal of this site is to not only generate benchmarks, but to also evaluate codes that solve phase field problems. We have a list of [suggested codes][suggested codes] that have been used to solve some of the benchmark problems.

# FAQ
<style>
h2 {
    color: black !important;
}

h3 {
    color: black !important;
}

h3 .heading-text {
    display: inline-block;
    transform: translateX(30px) !important;
}
</style>

## Which Code Should I Use to Solve my Phase Field Problem?

The right code for you depends on your familiarity with phase field methods and relevant software, hardware available and complexity of the phase field problem under consideration. We have a [list of phase field codes][suggested codes] and also a [list of benchmark results][benchmark results] that might help you evaluate which code might work best for you. Our objective is that the benchmarks will support users of the site in evaluating the suitability of codes for particular classes of phase field problems, but the user is the final arbiter in this process.

## I Don't Like One of the Benchmark Problems. Can I Help Fix it?

Yes. Your feedback on the benchmark problems is highly valued. The benchmarks are a moving target that you can contribute to. If you would like to propose a change or improvement then please raise it via [chat][chat] or as an [issue][issue]. The community will discuss the change and act on it if we can reach a consensus.

## Who is PFHub Intended For?

The Phase Field Community Hub is relevant to the diverse spectrum of phase-field community members, from newcomers to established experts in the theory, practice, and implementation of mesoscale models. The following “user stories” roughly sketch out how we intend this website to be of use to a few representative visitors.

## Novice Users

A novice (e.g., graduate student) may have been directed to choose a code and start modeling by an advisor or teacher, with no knowledge of phase field methods or our jargon. This user will not know exactly what they’re looking for. While basic education is beyond the scope of PFHub, we can help address the following questions.

- **What is “phase-field”?** To help this new user come up to speed, the website provides a set of [video lectures][video] by Prof. [Peter Voorhees][Peter] introducing the fundamental theory of phase-field methods.
- **How do I do it?** To help this new user launching simulations, the website provides a list of [suggested codes][suggested codes], briefly summarizing programming language, parallelization models, numerical methods, license, up-front and ongoing costs, and major dependencies.

## Advanced Users

An advanced user (e.g., early-career researcher) with experience in phase-field modeling might change positions or focus, and take a moment to survey the software landscape. This user will have some idea what they’re looking for, or specifically guarding against. Focus may be suitability to a specific task, or flexibility to address a wide variety of tasks. The researcher might be wondering…

- **Are my results in line?** To help the experienced user compare their performance against other users of the same code, the website provides the following:
    - A simple process for submitting simulation results with rapid feedback: new work appears in the graphs and tables on a test website, allowing iteration if the results are out of line.
    - Access to the source code for prior submissions
- **Is something better out there?** To help the experienced user drill down on options, the website provides the following:
    - A list of [suggested codes][suggested codes].
    - A dashboard showing how many results have been submitted using each code for each benchmark problem.
    - Visual summaries of relative performance of these codes on each benchmark problem.

## Expert Users

An expert user (e.g., software developer) experienced with phase-field models and numerical methods will be interested in upgrading their code, making it easier to use, more powerful, or able to run on evolving hardware and software platforms. The developer might be wondering…

- **Is my code competitive?** To help the developer compare apples to apples, the website provides the following:
    - List of available simulation results, with visualizations and ability to filter by code, platform, and author (fellow dev or user).
    - A Benchmark Problem using the method of manufactured solutions to help verify the discretization and numerical methods.
    - A responsive process for uploading simulation results when new benchmarks come out.

## Advisors (eg., faculty)

A faculty adviser who is continually having new researchers join their research group that are unfamiliar with the phase field method will be interested in having a collection of example problems with known, recorded solutions that their students can implement while learning.

- **Are New Researchers Solving Problems Correctly?** To best instruct new researchers, the website should provide:
    - Problems with all parameters, initial conditions, and boundary conditions defined.
    - Well established solutions using a range of different solution methods that new researchers can use for comparison.
    - Metrics from other codes showing computation times that new researchers can use to evaluate the efficiency of their solution.
- **Are They Learning A Range of Phase Field Problems?** To provide new researchers with a breadth of knowledge, rather than in just one area, the website should provide:
    - Problems covering a range of different materials phenomena.
    - Problems with increasing complexity.
    - Problems with unique aspects such as coupled mechanics or anisotropic surface energy.

[Andrea]: http://localhost:3000/community/#Andrea-Jokisaari
[Peter]: http://localhost:3000/community/#Peter-Voorhees
[Jon]: http://localhost:3000/community/#Jon-Guyer
[Jim]: http://localhost:3000/community/#Jim-Warren
[Olle]: http://localhost:3000/community/#Olle-Heinonen
[benchmark journal]: http://dx.doi.org/10.1016/j.commatsci.2016.09.022
[benchmark news]: http://chimad.northwestern.edu/news-events/articles/2016/PhaseField_BenchMark.html
[benchmark overview]: http://materials.typepad.com/mrs_meeting_scene/2017/11/tc05-uncertainty-quantification-in-multiscale-materials-simulation-1.html
[involvement guide]: http://localhost:3000/getinvolved
[community page]: http://localhost:3000/community
[suggested codes]: http://localhost:3000/suggestedcode
[benchmark results]: https://pfhub.github.io/pfhub-benchmarks/
[chat]: https://gitter.im/usnistgov/chimad-phase-field
[issue]: https://github.com/usnistgov/pfhub/issues/new
[video]: https://pages.nist.gov/pfhub/wiki/voorhees-lectures/

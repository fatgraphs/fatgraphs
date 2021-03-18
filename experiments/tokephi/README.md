# Tokephi

A tool to create images and videos of (token) networks using headless gephi


Note: Early prototype phase. Has issues. Needs refactoring, cleaning.


## Setup
Download `gephi-toolkit-0.9.2-all.jar` and `org-openide-util-lookup-RELEASE112.jar` and place them in a folder `libs`.
It would be nice to be able to pull these from some online source, but I currently don't know how to do that.


## How to run
You'll need a source CSV file, which is specified in `src/main/java/tokephi/App.java`
See `src/test/resources/tokenTransfers.csv` for an example.

```
./gradlew run
```

Tests:
```
./gradlew test
```

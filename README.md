# example-percy-python-appium
Example app used by the [Percy Python Appium tutorial](https://docs.percy.io/docs/python-appium-testing-tutorial) demonstrating Percy's Python Appium integration.

## Python Appium Tutorial

The tutorial assumes you're already familiar with Python and
[Appium](https://appium.io/) and focuses on using it with Percy. You'll still
be able to follow along if you're not familiar with Python Appium, but we won't
spend time introducing Python Appium concepts.


The tutorial also assumes you have [Node 12+ with
npm](https://nodejs.org/en/download/) and
[git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed.

### Step 1

Clone the example application and install dependencies:

```bash
$ git clone https://github.com/percy/example-percy-python-appium.git
$ cd example-percy-python-appium
$ make install
```

Example Android and iOS apps are provided in [`resources`](https://github.com/percy/example-percy-python-appium/blob/master/resources) folder. You can follow [`upload your app`](https://www.browserstack.com/docs/app-automate/appium/getting-started/python#2-upload-your-app) if using App Automate.

### Step 2

Sign in to Percy and create a new project. You can name the project "test-project" if you'd like. After
you've created the project, you'll be shown a token environment variable.

### Step 3

In the shell window you're working in, export the token environment variable:

**Unix**

``` shell
$ export PERCY_TOKEN="<your token here>"
```

**Windows**

``` shell
$ set PERCY_TOKEN="<your token here>"

# PowerShell
$ $Env:PERCY_TOKEN="<your token here>"
```

Note: Usually this would only be set up in your CI environment, but to keep things simple we'll
configure it in your shell so that Percy is enabled in your local environment.

### Step 4

Check out a new branch for your work in this tutorial (we'll call this branch
`tutorial-example`), then run tests & take screenshots:

``` shell
$ git checkout -b tutorial-example
# For Android
$ make test-android
# For iOS
$ make test-ios
```

This will run the app's Python Appium tests, which contain calls to create Percy screenshots. The screenshots
will then be uploaded to Percy for comparison. Percy will use the Percy token you used in **Step 2**
to know which organization and project to upload the screenshots to.

You can view the screenshots in Percy now if you want, but there will be no visual comparisons
yet. You'll see that Percy shows you that these screenshots come from your `tutorial-example` branch.

### Step 5

Use your text editor to edit `android.py` & `ios.py` and introduce some visual changes.

android.py: You can add an extra scroll before taking screenshots like:

``` shell
driver.executeScript("mobile: scrollGesture", params);
```

ios.py: You can update the key being sent to the textInput element.


### Step 6

Commit the change:

``` shell
$ git commit -am "Emphasize 'Clear completed' button"
```

### Step 7

Run the tests with screenshots again:

``` shell
# For Android
$ make test-android
# For iOS
$ make test-ios
```

This will run the tests again and take new screenshots of our modified application. The new screenshots
will be uploaded to Percy and compared with the previous screenshots, showing any visual diffs.

At the end of the test run output, you will see logs from Percy confirming that the screenshots were
successfully uploaded and giving you a direct URL to check out any visual diffs.

### Step 8

Visit your project in Percy and you'll see a new build with the visual comparisons between the two
runs. Click anywhere on the Build 2 row. You can see the original screenshots on the left, and the new
screenshots on the right.

Percy has highlighted what's changed visually in the app! Snapshots with the largest changes are
shown first You can click on the highlight to reveal the underlying screenshot.

If you scroll down, you'll see that no other test cases were impacted by our changes to the 'Clear
completed' button. The unchanged screenshots appear grouped together at the bottom of the list.

### Finished! 😀

From here, you can try making your own changes to the app and tests, if you like. If you do, re-run
the tests and you'll see any visual changes reflected in Percy.

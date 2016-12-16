# vis

<h1>Environment Setup</h1>
<ol>
  <li>Clone repository into directory of your choice and navigate to vis folder (hereto referenced as &lt;vis_home&gt;)</li>
  <li>Navigate to .../&lt;vis_home&gt;/ and run the command <code>sudo sh setup_env.sh</code>. The script
    <ul>
      <li>Removes and re-installs key libraries including git
      <li>Installs Chromium, Rust, Selenium, ChromeDriver, Torch (and packages).
      <li>Note that Torch will need extra configuration on a CUDA-enabled computer.
    </ul>
</ol>

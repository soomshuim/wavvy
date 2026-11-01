const task = await taskSpace("wavvy-2300-suno-regenerate");
const tabs = await task.tabs();
console.log(JSON.stringify(tabs.map(t => ({ label: t.label, url: t.url, openedBy: t.openedBy }))));
if (tabs.some(t => t.openedBy !== "agent")) { console.log("NON-AGENT TAB PRESENT; not finishing"); }
else { await task.finish({ keep: [] }); console.log("FINISHED space " + task.spaceId); }

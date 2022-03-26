#include "config.h"

using namespace tickout;

void
config::read(const std::string& path)
{
    std::ifstream f;
    f.open(path, std::ios::in);

    if (!f.is_open()) return;

    std::ostringstream ss;
    ss << f.rdbuf();

    auto parsed = json::parse(ss.str());

    if (parsed.contains("proxy")) {
        this->proxy_ = parsed["proxy"];
        if (this->proxy_) {
            this->proxy_address_ = parsed["proxy_address"];
        }
    }

    if (parsed.contains("user_agent")) {
        this->user_agent_ = parsed["user_agent"];
    }

    if (parsed.contains("chdir")) {
        const std::string chdir = parsed["chdir"];
        if (!chdir.empty()) {
            this->chdir_ = chdir;
        }
    }

    if (parsed.contains("bind"))
        this->bind_ = parsed["bind"];

    if (parsed.contains("port"))
        this->port_ = parsed["port"];
    
}

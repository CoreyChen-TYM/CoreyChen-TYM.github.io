#include <cstdint>
#include <fstream>
#include <stdexcept>
#include <string>

int main() {
    std::ifstream input("in.txt");
    std::ofstream output("output.pcm",
                         std::ios::binary | std::ios::trunc);
    if (!input || !output)
        throw std::runtime_error("Unable to open a file");

    const std::string marker = "Left channel: ";
    std::string line;
    while (std::getline(input, line)) {
        auto pos = line.find(marker);
        if (pos == std::string::npos) continue;
        auto value = static_cast<std::uint32_t>(
            std::stoul(line.substr(pos + marker.size()), nullptr, 16));
        // Write one 24-bit sample in little-endian byte order.
        for (unsigned shift = 0; shift < 24; shift += 8)
            output.put(static_cast<char>((value >> shift) & 0xff));
        if (!output) throw std::runtime_error("Write failed");
    }
    if (input.bad()) throw std::runtime_error("Read failed");
    output.close();
    if (!output) throw std::runtime_error("Close failed");
}

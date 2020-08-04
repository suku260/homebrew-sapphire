class Sapphire < Formula
  desc ""
  homepage "http://www.sapphirelang.info"
  url "http://www.github.com/suku260/Sapphire"
  version "0.5.1"
  sha256 "afd3e590825ddf05ed613cb34bd001e3afef801b1caaeb8f49057a1e95513a3a"
  
  license "bsd"

  # depends_on "cmake" => :build

  def install
    bin.install "Sapphire"
    # ENV.deparallelize
    system "./configure", "--disable-debug",
                          "--disable-dependency-tracking",
                          "--disable-silent-rules",
                          "--prefix=#{prefix}"
    # system "cmake", ".", *std_cmake_args
    system "make", "install"
  end

  test do
    assert_equal "homebrew", shell_output("#{bin}/sapphire -c 'echo homebrew'").chomp
    system bin/"sapphire", "-c", "printf -v hello -- '%s'"
  end
end
